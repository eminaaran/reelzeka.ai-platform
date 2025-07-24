from django.contrib import admin
from .models import Belge, ChatMessage

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
