import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from .models import Topic, Question, Choice

# .env dosyasındaki değişkenleri yükle
load_dotenv()

class SoruUretici:
    def __init__(self):
        try:
            gemini_api_key = os.environ.get("GEMINI_API_KEY")
            if not gemini_api_key:
                raise ValueError("GEMINI_API_KEY ortam değişkeni bulunamadı.")
            
            genai.configure(api_key=gemini_api_key)
            
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-pro-latest",
                generation_config={"response_mime_type": "application/json"}
            )
        except Exception as e:
            raise Exception(f"Gemini API istemcisi başlatılamadı: {e}")

    def _get_prompt_template(self):
        return """
        Sen, ÖSYM standartlarında, YKS öğrencileri için sorular üreten bir eğitim uzmanısın.
        Görevin, aşağıda verilen konu ve ders bilgisine %100 bağlı kalarak, belirtilen formatta TEK BİR soru oluşturmaktır.
        Cevap olarak SADECE ve SADECE istenen JSON nesnesini ver, başka hiçbir açıklama, metin veya markdown formatı (`json` bloğu gibi) ekleme.

        Ders: {ders_adi}
        Konu: {konu_adi}

        JSON Çıktı Formatı:
        {{
          "soru_metni": "Buraya sorunun metnini yaz.",
          "secenekler": [
            {{ "metin": "A şıkkının metni", "dogru_mu": false }},
            {{ "metin": "B şıkkının metni", "dogru_mu": false }},
            {{ "metin": "C şıkkının metni", "dogru_mu": true }},
            {{ "metin": "D şıkkının metni", "dogru_mu": false }},
            {{ "metin": "E şıkkının metni", "dogru_mu": false }}
          ],
          "zorluk_derecesi": "orta",
          "aciklama": "Bu kısma soru ve doğru cevap ile ilgili kısa bir açıklama yaz."
        }}
        """

    def generate_and_save_question(self, topic_id: int):
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            print(f"Hata: ID'si {topic_id} olan bir konu bulunamadı.")
            return None

        ders_adi = topic.subject.name
        konu_adi = topic.name

        prompt = self._get_prompt_template().format(ders_adi=ders_adi, konu_adi=konu_adi)

        print(f"'{konu_adi}' konusu için Google Gemini'ye istek gönderiliyor...")

        try:
            response = self.model.generate_content(prompt)
            soru_data = json.loads(response.text)

            # Veritabanına kaydet
            yeni_soru = Question.objects.create(
                topic=topic,
                text=soru_data['soru_metni'],
                difficulty=soru_data.get('zorluk_derecesi', 'medium'),
                explanation=soru_data.get('aciklama', '')
            )

            for secenek_data in soru_data['secenekler']:
                Choice.objects.create(
                    question=yeni_soru,
                    text=secenek_data['metin'],
                    is_correct=secenek_data['dogru_mu']
                )

            print(f"Başarılı! ID'si {yeni_soru.id} olan yeni bir soru oluşturuldu ve '{topic.name}' konusuna bağlandı.")
            return yeni_soru

        except Exception as e:
            print(f"Soru üretimi veya kaydı sırasında bir hata oluştu: {e}")
            # 'response' değişkeni tanımlı olmayabilir, bu yüzden kontrol ekliyoruz.
            raw_response = "Cevap alınamadı."
            if 'response' in locals() and hasattr(response, 'text'):
                raw_response = response.text
            print(f"Gemini'den gelen ham cevap: {raw_response}")
            return None