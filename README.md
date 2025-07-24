# ReelZeka.ai - Yapay Zeka Destekli YKS Öğrenme Platformu


**ReelZeka.ai**, Türkiye'deki üniversite giriş sınavı (YKS) hazırlık sürecini modern teknolojilerle dönüştürmeyi hedefleyen, Django ve React ile geliştirilmiş, yapay zeka tabanlı bir eğitim platformudur. Öğrencilere kişiselleştirilmiş bir öğrenme deneyimi sunarak, sadece "ne" çalışmaları gerektiğini değil, "nasıl" daha verimli çalışacaklarını da öğretir.

---

## ✨ Projenin Vizyonu

Klasik eğitim metotlarının ötesine geçerek, her öğrencinin kendine özgü öğrenme stilini ve ihtiyaçlarını anlayan bir "dijital koç" yaratmak. Bu platform, RAG (Retrieval-Augmented Generation) teknolojisi sayesinde YKS müfredatına %100 uyumlu, güvenilir ve "nokta atışı" cevaplar sunarken, aynı zamanda Atomic Habits gibi verimlilik metodolojilerinden ilham alan araçlarla öğrencinin motivasyonunu ve çalışma disiplinini artırmayı hedefler.

---

## 🚀 Temel Özellikler

*   **🧠 Akıllı RAG Asistanı:** Yüklenen ders notları (.txt, .pdf) üzerinden, YKS müfredatına özel olarak eğitilmiş, halüsinasyon riski azaltılmış bir yapay zeka asistanı.
*   **📚 Dinamik İçerik Yönetimi:** Django Admin paneli üzerinden sisteme kolayca yeni ders notları ve materyaller ekleyebilme.
*   **🗓️ İlerleme Takibi:** (Geliştirme Aşamasında) Atomic Habits'ten ilham alan, tamamlanan görevleri ve çalışma serilerini gösteren interaktif bir takvim.
*   **🍅 Pomodoro Sayacı:** (Geliştirme Aşamasında) Odaklanmayı artıran, özelleştirilebilir Pomodoro çalışma seansları.
*   **📝 Test ve Denemeler:** (Geliştirme Aşamasında) Branş bazlı mini testler ve deneme sınavları ile sürekli pratik imkanı.
*   **🃏 Bilgi Kartları:** (Geliştirme Aşamasında) Quizlet tarzı bilgi kartları ile hızlı ve etkili tekrar seansları.
*   **Modern ve Akıcı Arayüz:** Django (Backend API) ve React (Frontend SPA) mimarisi sayesinde hızlı, dinamik ve kullanıcı dostu bir deneyim.

---

## 💻 Kullanılan Teknolojiler

| Kategori      | Teknoloji                                                                                              |
|---------------|--------------------------------------------------------------------------------------------------------|
| **Backend**   | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django&logoColor=white) |
| **Frontend**  | ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white) ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white) |
| **AI & ML**   | ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-FFFFFF?style=for-the-badge) |
| **Veritabanı**| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) ![ChromaDB](https://img.shields.io/badge/ChromaDB-5A46F3?style=for-the-badge)  |
| **Araçlar**   | ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white) ![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white) |

---

## ⚙️ Kurulum ve Başlatma

Bu projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

### Ön Gereksinimler
*   Python 3.10+
*   Node.js ve npm
*   Git

### Backend (Django) Kurulumu
```bash
# 1. Projeyi klonlayın
git clone https://github.com/eminaaran/reelzeka.ai-platform.git
cd reelzeka.ai-platform

# 2. Sanal ortam oluşturun ve aktive edin
python -m venv venv
# Windows için:
venv\Scripts\activate
# macOS/Linux için:
# source venv/bin/activate

# 3. Gerekli Python kütüphanelerini kurun
pip install -r requirements.txt

# 4. .env dosyasını oluşturun ve API anahtarınızı ekleyin
# Ana dizinde .env adında bir dosya oluşturun ve içine şunu yazın:
# OPENAI_API_KEY="sk-..."

# 5. Veritabanını oluşturun ve admin kullanıcısı yaratın
python manage.py migrate
python manage.py createsuperuser

# 6. Django sunucusunu başlatın
python manage.py runserver
# Backend şimdi http://127.0.0.1:8000 adresinde çalışıyor olacak
