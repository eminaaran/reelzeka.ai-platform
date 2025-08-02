from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Belge, ChatMessage, Subject, Topic, Question, Choice, Test, TestQuestion
from .forms import TestWizardForm
from import_export.admin import ImportExportModelAdmin
from import_export import resources
import random

@admin.register(Belge)
class BelgeAdmin(admin.ModelAdmin):
    list_display = ('ders_adi', 'dosya', 'yuklenme_tarihi', 'indekslendi_mi')
    list_filter = ('indekslendi_mi', 'ders_adi')
    search_fields = ('ders_adi', 'dosya__name')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'prompt', 'created_at')
    list_filter = ('user',)
    search_fields = ('prompt', 'response')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description')
    search_fields = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id','subject', 'name', 'description')
    list_filter = ('subject',)
    search_fields = ('name', 'subject__name')

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question

class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ('topic', 'text', 'difficulty', 'created_at', 'status') # status eklendi
    list_filter = ('topic', 'difficulty', 'status') # status eklendi
    search_fields = ('text', 'topic__name')
    actions = ['approve_questions']

    def approve_questions(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Seçilen sorular başarıyla onaylandı.")
    approve_questions.short_description = "Seçilen soruları onayla"

admin.site.register(Question, QuestionAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'created_by', 'created_at', 'duration', 'is_public')
    list_filter = ('type', 'is_public', 'created_by')
    search_fields = ('title', 'description')
    change_form_template = "admin/core/test/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/wizard/',
                self.admin_site.admin_view(self.wizard_view),
                name='test-wizard',
            ),
        ]
        return custom_urls + urls

    def wizard_view(self, request, object_id):
        test = self.get_object(request, object_id)
        if request.method == 'POST':
            form = TestWizardForm(request.POST)
            if form.is_valid():
                topics = form.cleaned_data['topics']
                num_questions = form.cleaned_data['num_questions']
                # ... (zorluk dağılımı mantığı buraya eklenecek)

                # Mevcut soruları temizle
                test.questions.clear()

                # Yeni soruları seç ve ekle
                question_pool = list(Question.objects.filter(
                    topic__in=topics,
                    status='approved' # Sadece onaylanmış sorular
                ))
                
                if len(question_pool) < num_questions:
                    messages.warning(request, f"Havuzda yeterli soru yok. {len(question_pool)} adet soru bulundu, {num_questions} adet istendi.")
                    return redirect(request.path)

                selected_questions = random.sample(question_pool, num_questions)
                test.questions.add(*selected_questions)

                messages.success(request, f'{num_questions} adet soru teste başarıyla eklendi.')
                return redirect(f'/admin/core/test/{object_id}/change/')
        else:
            form = TestWizardForm()

        context = {
            'opts': self.model._meta,
            'form': form,
            'title': 'Test Oluşturma Sihirbazı',
            'original': test,
        }
        return render(request, 'admin/core/test/wizard_form.html', context)

admin.site.register(Test, TestAdmin)