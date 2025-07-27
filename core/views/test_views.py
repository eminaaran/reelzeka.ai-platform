from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Subject, Topic, Test, UserTestResult, Question, Choice
from ..serializers.test_serializers import (
    SubjectSerializer,
    TopicSerializer,
    TestListSerializer,
    TestDetailSerializer,
    TestSubmissionSerializer,
    TestResultSerializer
)

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.AllowAny]

class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Sadece public testleri göster"""
        queryset = Test.objects.filter(is_public=True)
        if not queryset.exists():
            # Eğer test yoksa, örnek bir test oluştur
            from django.contrib.auth.models import User
            admin_user = User.objects.filter(is_superuser=True).first()
            if admin_user:
                test = Test.objects.create(
                    title='TYT Matematik Mini Deneme',
                    description='20 dakikalık mini deneme testi',
                    type='practice',
                    created_by=admin_user,
                    duration=20,
                    is_public=True # Örnek testin public olduğundan emin ol
                )
                # Örnek teste bir soru ekle
                # Varsayılan bir konu ve ders oluştur veya bul
                default_subject, created = Subject.objects.get_or_create(name='Genel', defaults={'description': 'Genel Konular'})
                default_topic, created = Topic.objects.get_or_create(subject=default_subject, name='Varsayılan Konu', defaults={'description': 'Varsayılan Açıklama'})

                question = Question.objects.create(
                    topic=default_topic,  # veya uygun bir topic seçin
                    text='Örnek Soru 1',
                    difficulty='easy'
                )
                # Örnek soruya seçenekler ekle
                Choice.objects.create(question=question, text='Seçenek A', is_correct=True)
                Choice.objects.create(question=question, text='Seçenek B', is_correct=False)
                Choice.objects.create(question=question, text='Seçenek C', is_correct=False)
                Choice.objects.create(question=question, text='Seçenek D', is_correct=False)

                test.questions.add(question, through_defaults={'order': 1}) # Sıra numarası ekle
                queryset = Test.objects.filter(is_public=True)
        return queryset.order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestDetailSerializer
        return TestListSerializer

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        test = self.get_object()
        serializer = TestSubmissionSerializer(data=request.data)
        
        if not serializer.is_valid():
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        answers = serializer.validated_data['answers']
        correct_count = 0
        total_questions = test.questions.all().count()

        # Cevapları kontrol et
        for question_id, answer_text in answers.items():
            question = test.questions.get(id=question_id)
            if question.choices.filter(text=answer_text, is_correct=True).exists():
                correct_count += 1

        # Skoru hesapla
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        # Sonucu kaydet
        result = UserTestResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            duration_taken=request.data.get('duration_taken', 0)
        )

        serializer = TestResultSerializer(result)
        return Response(serializer.data)
