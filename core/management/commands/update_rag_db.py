# core/management/commands/update_rag_db.py

from django.core.management.base import BaseCommand
from django.conf import settings # MEDIA_ROOT'u almak için
from core.models import Belge

# RAG sistemimizin mantığını içeren kütüphaneler
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os

class Command(BaseCommand):
    help = 'Admin panelinden eklenen ve henüz işlenmemiş belgeleri RAG veritabanına ekler.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('>>> Yeni belgeler RAG veritabanına ekleniyor...'))

        # 1. Adım: Henüz işlenmemiş ("indekslenmemiş") belgeleri veritabanından bul.
        yeni_belgeler = Belge.objects.filter(indekslendi_mi=False)
        
        if not yeni_belgeler.exists():
            self.stdout.write(self.style.SUCCESS('-> İşlenecek yeni belge bulunamadı.'))
            return # Yapacak bir şey yok, komutu bitir.

        self.stdout.write(f"-> {yeni_belgeler.count()} adet yeni belge bulundu. İşlem başlatılıyor...")

        # 2. Adım: RAG veritabanına (ChromaDB) bağlan.
        try:
            embeddings = OpenAIEmbeddings()
            CHROMA_PATH = os.path.join(settings.BASE_DIR, "chroma_db")
            vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"HATA: ChromaDB'ye bağlanılamadı: {e}"))
            return

        # 3. Adım: Her yeni belge için döngü başlat ve RAG işlemlerini yap.
        for belge in yeni_belgeler:
            self.stdout.write(f"--- '{belge}' işleniyor... ---")
            
            # Yüklenen dosyanın tam yolunu al
            dosya_yolu = belge.dosya.path
            
            try:
                # A. Belgeyi oku
                loader = TextLoader(dosya_yolu, encoding="utf-8")
                documents = loader.load()

                # B. Metni parçalara ayır
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
                metin_parcalari = text_splitter.split_documents(documents)
                
                # C. Parçaları vektörleştir ve ChromaDB'ye EKLE
                if metin_parcalari:
                    vectorstore.add_documents(metin_parcalari)
                    self.stdout.write(self.style.SUCCESS(f"   - {len(metin_parcalari)} parça ChromaDB'ye eklendi."))
                
                # D. Başarılı olursa, belgeyi 'indekslendi' olarak işaretle ki bir daha işlenmesin.
                belge.indekslendi_mi = True
                belge.save()
                
                self.stdout.write(self.style.SUCCESS(f"   - '{belge}' başarıyla işlendi ve veritabanında işaretlendi."))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"HATA: '{belge}' işlenirken bir sorun oluştu: {e}"))
        
        self.stdout.write(self.style.SUCCESS('>>> Güncelleme işlemi tamamlandı!'))