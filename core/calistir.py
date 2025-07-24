# Gerekli kütüphaneleri ve modülleri programımıza dahil ediyoruz.
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma # FAISS yerine Chroma
from pathlib import Path

# --- AŞAMA 0: TEMEL AYARLAR VE YOL TANIMLARI ---
# Bu kod, bu dosyanın ('calistir.py') bulunduğu yerin bir üstündeki
# ana proje klasörünü (yani 'manage.py'nin olduğu yeri) bulur.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Global değişken (RAG zincirini hafızada tutmak için)
qa_chain_instance = None

# --- AŞAMA 1: RAG SİSTEMİNİ KURAN FONKSİYON ---
def initialize_rag_chain():
    """
    Bu fonksiyon, RAG zincirini (veri, vektörler, LLM, prompt) kurar.
    Kalıcı bir ChromaDB veritabanı kullanır. Veritabanı boşsa ilk verileri yükler.
    Uygulama başladığında SADECE BİR KEZ çağrılması hedeflenir.
    """
    global qa_chain_instance
    print(">>> RAG Zinciri (ChromaDB) başlatılıyor...")

    embeddings = OpenAIEmbeddings()

    # Kalıcı ChromaDB istemcisini oluştur. Veritabanını 'chroma_db' klasöründe saklayacak.
    CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # Veritabanında zaten belge var mı diye kontrol et.
    # Eğer hiç belge yoksa (ilk kurulum), o zaman dosyaları oku ve ekle.
    if vectorstore._collection.count() == 0:
        print("-> Vektör deposu boş. 'data' klasöründen ilk veriler yükleniyor...")
        
        DATA_KLASORU = os.path.join(BASE_DIR, 'data')
        if not os.path.exists(DATA_KLASORU) or not os.listdir(DATA_KLASORU):
             print(f"XXX UYARI: 'data' klasörü boş veya bulunamadı! Lütfen içine .txt dosyalarınızı ekleyin. XXX")
             # Zincir boş bir şekilde kurulacak ama cevap veremeyecek.
        else:
            loader = DirectoryLoader(DATA_KLASORU, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
            metin_parcalari = text_splitter.split_documents(documents)
            
            if metin_parcalari:
                print(f"   - {len(metin_parcalari)} adet metin parçası veritabanına ekleniyor...")
                vectorstore.add_documents(metin_parcalari)
                print("   - İlk veriler başarıyla eklendi.")

    # Retriever ve geri kalan zincir kurulumu
    retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
    
    prompt_template = """
    Sen, YKS müfredatına hakim, yardımsever bir yapay zeka asistanısın. 
    Görevin, sadece ve sadece sana verilen aşağıdaki "BAĞLAM" bölümündeki bilgileri kullanarak öğrencinin "SORU"sunu cevaplamaktır.
    Eğer cevap bağlamda açıkça belirtilmiyorsa, "Bu konuda sağlanan metinlerde bir bilgi bulamadım." de. Asla tahmin yürütme veya bilgi uydurma.
    Cevabını bir öğretmen gibi açık ve anlaşılır bir dille ifade et.
    ---
    BAĞLAM: {context}
    ---
    SORU: {question}
    ---
    CEVAP:
    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain_instance = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": PROMPT}
    )
    print(">>> RAG Zinciri (ChromaDB) kullanıma hazır!")

# --- AŞAMA 2: SORULARI CEVAPLAYAN FONKSİYON ---
def rag_ile_cevap_ver(kullanici_sorusu: str) -> str:
    """
    Django view'ımızın çağıracağı ana fonksiyon budur.
    Kullanıcıdan gelen soruyu alır ve RAG zincirini kullanarak cevap üretir.
    """
    global qa_chain_instance
    
    # Eğer RAG zinciri henüz hafızaya yüklenmemişse (uygulama yeni başladıysa), yükle.
    if qa_chain_instance is None:
        initialize_rag_chain()

    if not kullanici_sorusu:
        return "Lütfen bir soru yazın."
    
    # qa_chain_instance hala None ise, kurulumda bir hata olmuştur.
    if qa_chain_instance is None:
        return "Üzgünüm, RAG sistemi başlatılamadı. Lütfen sunucu loglarını kontrol edin."
    
    print(f"\n>>> RAG zinciri sorgulanıyor... Soru: '{kullanici_sorusu}'")
    
    sonuc = qa_chain_instance.invoke(kullanici_sorusu)
    return sonuc["result"]


# --- AŞAMA 3: BU DOSYAYI TEK BAŞINA TEST ETMEK İÇİN KULLANILAN BÖLÜM ---
if __name__ == '__main__':
    print("="*50)
    print("calistir.py dosyası tek başına test modunda çalıştırıldı.")
    print("="*50)
    
    # Test için sistemi bir kere başlat.
    initialize_rag_chain()
    
    # Senin eski while döngün, artık sadece test için burada.
    while True:
        soru = input("\nTest sorunuzu yazın (çıkmak için 'çıkış'): ")
        if soru.lower() == 'çıkış':
            break
        
        cevap = rag_ile_cevap_ver(kullanici_sorusu=soru)
        print("\nCEVAP:")
        print(cevap)