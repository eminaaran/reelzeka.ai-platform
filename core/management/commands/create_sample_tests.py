from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Subject, Topic, Question, Choice, Test, TestQuestion

class Command(BaseCommand):
    help = 'Creates sample test data'

    def handle(self, *args, **kwargs):
        # Create a subject
        subject, _ = Subject.objects.get_or_create(
            name="Türk Dili ve Edebiyatı",
            description="Türk Edebiyatı ve dil bilgisi konuları"
        )

        # Create topics
        topics_data = [
            {
                "name": "Dil Bilgisi",
                "description": "Türkçe dil bilgisi konuları"
            },
            {
                "name": "Edebi Akımlar",
                "description": "Türk ve Dünya Edebiyatındaki akımlar"
            }
        ]

        topics = []
        for topic_data in topics_data:
            topic, _ = Topic.objects.get_or_create(
                subject=subject,
                name=topic_data["name"],
                description=topic_data["description"]
            )
            topics.append(topic)

        # Create questions
        questions_data = [
            {
                "topic": topics[0],
                "text": "Aşağıdaki cümlelerin hangisinde yazım yanlışı yapılmıştır?",
                "difficulty": "medium",
                "explanation": "Türkçede 'de' bağlacı ayrı yazılır ancak hal eki olan '-de' bitişik yazılır.",
                "choices": [
                    {"text": "Kitabı masada unutmuş.", "is_correct": False},
                    {"text": "O da bizimle gelecek.", "is_correct": False},
                    {"text": "Bahçede çiçekler açmış.", "is_correct": False},
                    {"text": "Sokakta ki kalabalık artıyor.", "is_correct": True}
                ]
            },
            {
                "topic": topics[1],
                "text": "Aşağıdakilerden hangisi Servet-i Fünun edebiyatının özelliklerinden değildir?",
                "difficulty": "medium",
                "explanation": "Halk için sanat anlayışı Servet-i Fünun'un değil, Milli Edebiyat akımının özelliğidir.",
                "choices": [
                    {"text": "Sanat için sanat anlayışı", "is_correct": False},
                    {"text": "Ağır ve süslü bir dil kullanımı", "is_correct": False},
                    {"text": "Halk için sanat anlayışı", "is_correct": True},
                    {"text": "Fransız edebiyatının etkisi", "is_correct": False}
                ]
            },
            {
                "topic": topics[0],
                "text": "Aşağıdaki cümlelerin hangisinde özne yoktur?",
                "difficulty": "easy",
                "explanation": "Özne, yüklemin bildirdiği işi yapan öğedir. 'Yağmur yağıyor' cümlesinde özne 'yağmur'dur.",
                "choices": [
                    {"text": "Yağmur yağıyor.", "is_correct": False},
                    {"text": "Akşama kadar ders çalıştı.", "is_correct": True},
                    {"text": "Çocuklar parkta oynuyor.", "is_correct": False},
                    {"text": "Kuşlar gökyüzünde süzülüyor.", "is_correct": False}
                ]
            }
        ]

        created_questions = []
        for q_data in questions_data:
            question = Question.objects.create(
                topic=q_data["topic"],
                text=q_data["text"],
                difficulty=q_data["difficulty"],
                explanation=q_data["explanation"]
            )
            
            for c_data in q_data["choices"]:
                Choice.objects.create(
                    question=question,
                    text=c_data["text"],
                    is_correct=c_data["is_correct"]
                )
            
            created_questions.append(question)

        # Create a test
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            test = Test.objects.create(
                title="Türkçe Deneme Testi",
                description="Dil bilgisi ve edebiyat konularını içeren kısa bir test",
                type="practice",
                created_by=admin_user,
                duration=15,
                is_public=True
            )

            # Add questions to test
            for i, question in enumerate(created_questions):
                TestQuestion.objects.create(
                    test=test,
                    question=question,
                    order=i
                )

            self.stdout.write(self.style.SUCCESS('Successfully created sample test data'))
        else:
            self.stdout.write(self.style.ERROR('No admin user found. Please create a superuser first.'))
