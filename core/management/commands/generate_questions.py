from django.core.management.base import BaseCommand
from core.models import Topic, Question, Choice
import random
import json

# Bu fonksiyon, gerçek bir LLM çağrısını simüle eder.
# Normalde burada OpenAI, Gemini veya başka bir LLM API'sine istek atılır.
def generate_mock_question_from_llm(topic):
    mock_responses = [
        {
            "soru": f"{topic.name} hakkında rastgele bir soru metni?",
            "secenekler": [
                {"metin": "Doğru Cevap", "dogru_mu": True},
                {"metin": "Yanlış Cevap 1", "dogru_mu": False},
                {"metin": "Yanlış Cevap 2", "dogru_mu": False},
                {"metin": "Yanlış Cevap 3", "dogru_mu": False}
            ],
            "aciklama": "Bu sorunun açıklamasıdır."
        },
        {
            "soru": f"{topic.name} ile ilgili başka bir soru?",
            "secenekler": [
                {"metin": "Seçenek A", "dogru_mu": False},
                {"metin": "Seçenek B (Doğru)", "dogru_mu": True},
                {"metin": "Seçenek C", "dogru_mu": False},
                {"metin": "Seçenek D", "dogru_mu": False}
            ],
            "aciklama": "Bu, doğru cevabın neden B olduğunun açıklamasıdır."
        }
    ]
    # Rastgele bir tanesini seçip döndür
    return random.choice(mock_responses)

class Command(BaseCommand):
    help = 'Belirtilen bir konu (Topic) için yapay zeka kullanarak otomatik olarak sorular üretir.'

    def add_arguments(self, parser):
        parser.add_argument('--topic_id', type=int, help='Soruların üretileceği Topic ID\'si.', required=True)
        parser.add_argument('--count', type=int, help='Üretilecek soru sayısı.', default=10)

    def handle(self, *args, **options):
        topic_id = options['topic_id']
        count = options['count']

        try:
            topic = Topic.objects.get(pk=topic_id)
        except Topic.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Topic with ID "{topic_id}" does not exist.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Generating {count} questions for topic: "{topic.name}"...'))

        for i in range(count):
            self.stdout.write(f'  -> Generating question {i+1}/{count}...')
            
            # LLM'den soru üret (Simülasyon)
            generated_data = generate_mock_question_from_llm(topic)

            # Gelen veriyi veritabanına kaydet
            try:
                question = Question.objects.create(
                    topic=topic,
                    text=generated_data['soru'],
                    explanation=generated_data.get('aciklama', ''),
                    difficulty='medium',  # Varsayılan veya LLM'den gelen
                    status='pending' # Onay bekliyor olarak kaydet
                )

                for choice_data in generated_data['secenekler']:
                    Choice.objects.create(
                        question=question,
                        text=choice_data['metin'],
                        is_correct=choice_data['dogru_mu']
                    )
                
                self.stdout.write(self.style.SUCCESS(f'    Successfully created question: "{question.text[:30]}..."'))

            except (KeyError, TypeError) as e:
                self.stdout.write(self.style.ERROR(f'    Error processing generated data: {e}'))
                self.stdout.write(self.style.WARNING(f'    Skipping this question. Data: {generated_data}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'Finished generating {count} questions for "{topic.name}".'))
