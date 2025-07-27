from django.contrib import admin
from .models import Belge, ChatMessage, Subject, Topic, Question, Choice, Test, TestQuestion

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
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'description')
    list_filter = ('subject',)
    search_fields = ('name', 'subject__name')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'text', 'difficulty', 'created_at')
    list_filter = ('topic', 'difficulty')
    search_fields = ('text', 'topic__name')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'created_by', 'created_at', 'duration', 'is_public')
    list_filter = ('type', 'is_public', 'created_by')
    search_fields = ('title', 'description')
