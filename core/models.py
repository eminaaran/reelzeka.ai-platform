from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Django'ya 'Belge' adında bir veri modeli (tablo şablonu) oluşturmasını söylüyoruz.
class Belge(models.Model):
    # Her belgenin bir ders adı olacak. Bu metin en fazla 100 karakter olabilir.
    ders_adi = models.CharField(max_length=100, help_text="Örn: Edebiyat, Tarih")
    
    # Her belgenin bir dosyası olacak. Yüklenen dosyalar 'media/belgeler/' klasörüne kaydedilecek.
    dosya = models.FileField(upload_to='belgeler/', help_text=".txt uzantılı olmalı")
    
    # Belgenin ne zaman yüklendiğini otomatik olarak kaydeder.
    yuklenme_tarihi = models.DateTimeField(auto_now_add=True)
    
    # Bu dosyanın RAG veritabanına eklenip eklenmediğini takip etmek için bir evet/hayır alanı.
    indekslendi_mi = models.BooleanField(default=False, help_text="Bu dosya RAG veritabanına eklendi mi?")

    # Admin panelinde her belgeyi daha anlaşılır bir şekilde göstermek için.
    def __str__(self):
        # dosya.name, dosyanın tam yolunu verir (örn: belgeler/tarih_notlari.txt)
        # Biz sadece dosya adını göstermek için küçük bir işlem yapıyoruz.
        dosya_adi = self.dosya.name.split('/')[-1]
        return f"{self.ders_adi} - {dosya_adi}"

# YENİ MODEL: Sohbet Mesajları
class ChatMessage(models.Model):
    # Mesajı gönderen kullanıcı. User silinirse, mesajları da silinir (CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Kullanıcının sorduğu soru.
    prompt = models.TextField()
    # Yapay zekanın verdiği cevap.
    response = models.TextField()
    # Mesajın oluşturulma tarihi. Otomatik olarak o anki zamanı kaydeder.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Admin panelinde mesajı daha okunaklı göstermek için.
        return f'{self.user.username}: {self.prompt[:50]}'