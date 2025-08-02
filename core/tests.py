from django.test import TestCase

# Create your tests here.
from django.contrib import admin
from .models import Test, Soru, Secenek

# Seçeneklerin, Soru ekleme sayfasının içinde görünmesini sağlamak için
# StackedInline veya TabularInline kullanmak çok pratiktir.
class SecenekInline(admin.TabularInline):
    model = Secenek
    extra = 4 # Varsayılan olarak 4 tane boş seçenek alanı gösterir

# Soru modelini admin arayüzünde yapılandırmak için
class SoruAdmin(admin.ModelAdmin):
    inlines = [SecenekInline] # Soru eklerken seçenekleri de ekleyebilmemizi sağlar
    list_display = ('metin', 'test', 'id') # Soru listesinde hangi alanların görüneceği
    list_filter = ('test',) # Teste göre filtreleme yapabilmemizi sağlar

# Test modelini admin arayüzünde yapılandırmak için
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'id')
    search_fields = ('title', 'subject') # Başlık ve konuya göre arama yapabilmemizi sağlar


# Modelleri ve özel admin sınıflarını kaydet
admin.site.register(Test, TestAdmin)
admin.site.register(Soru, SoruAdmin)
# Seçenek modelini direkt kaydetmeye gerek yok, çünkü Soru'nun içinde yöneteceğiz.
# Ama istersen ayrı olarak da kaydedebilirsin: admin.site.register(Secenek)
