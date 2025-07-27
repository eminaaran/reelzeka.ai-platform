# core/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# Serializer'ları import etmemiz gerekiyor
from .serializers import (
    UserRegistrationSerializer, RagQuerySerializer, UserSerializer,
    SubjectSerializer, TopicSerializer, QuestionSerializer,
    TestListSerializer, TestDetailSerializer, UserTestResultSerializer
)
from .models import Subject, Topic, Question, Test, UserTestResult

# RAG sistemimizi import ediyoruz
try:
    from .calistir import rag_ile_cevap_ver
except ImportError:
    def rag_ile_cevap_ver(kullanici_sorusu, ders_adi=None):
        print("UYARI: RAG sistemi (calistir.py) yüklenemedi.")
        return "HATA: RAG sistemi yüklenemedi."

# --- API View'ları ---

@ensure_csrf_cookie
def get_csrf_token(request):
    """React'in CSRF cookie'sini almasını sağlayan basit view."""
    return JsonResponse({"detail": "CSRF cookie set"})

class UserRegistrationAPIView(APIView):
    """Yeni kullanıcı kaydı için API endpoint'i."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    """Kullanıcı girişi için API endpoint'i."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({"error": "Geçersiz kullanıcı adı veya şifre"}, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    """Kullanıcı çıkışı için API endpoint'i."""
    def post(self, request):
        logout(request)
        return Response({"success": "Başarıyla çıkış yapıldı"}, status=status.HTTP_200_OK)

class CheckAuthAPIView(APIView):
    """Kullanıcının giriş yapıp yapmadığını kontrol eden endpoint."""
    def get(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        return Response({"error": "Giriş yapılmamış"}, status=status.HTTP_401_UNAUTHORIZED)

from django.contrib.auth.models import User
from rest_framework import generics, permissions

# ... (diğer importlar)

# Admin için özel bir permission class'ı
class IsAdminUser(permissions.BasePermission):
    """Sadece admin (is_staff=True) kullanıcıların erişimine izin verir."""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

# --- API View'ları ---

# ... (mevcut view'lar)

class UserListView(generics.ListAPIView):
    """Admin paneli için tüm kullanıcıları listeleyen view."""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # Sadece adminler erişebilir

class RagQueryAPIView(APIView):
    """RAG sistemine soru sormak için API endpoint'i."""
    def post(self, request):
        serializer = RagQuerySerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data.get('question')
            ders = serializer.validated_data.get('ders')
            try:
                answer = rag_ile_cevap_ver(kullanici_sorusu=question, ders_adi=ders)
                return Response({"answer": answer})
            except Exception as e:
                return Response({"error": f"RAG sisteminde hata: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Test Modülü Views
class SubjectViewSet(viewsets.ModelViewSet):
    """
    Konu başlıkları için viewset.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True)
    def topics(self, request, pk=None):
        subject = self.get_object()
        topics = subject.topics.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

class TopicViewSet(viewsets.ModelViewSet):
    """
    Alt konular için viewset.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True)
    def questions(self, request, pk=None):
        topic = self.get_object()
        questions = topic.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class TestViewSet(viewsets.ModelViewSet):
    """
    Testler için viewset.
    list: Tüm testleri listeler
    retrieve: Tek bir testin detaylarını gösterir
    create: Yeni test oluşturur
    update: Mevcut testi günceller
    delete: Testi siler
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Eğer kullanıcı admin ise tüm testleri, değilse sadece public testleri göster
        if self.request.user.is_staff:
            return Test.objects.all()
        return Test.objects.filter(is_public=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return TestListSerializer
        return TestDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Test sonuçlarını kaydetmek için endpoint.
        """
        test = self.get_object()
        
        # Request'ten gelen veriler
        answers = request.data.get('answers', [])
        duration = request.data.get('duration')  # Saniye cinsinden
        score = request.data.get('score')

        # Test sonucunu kaydet
        test_result = UserTestResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            duration_taken=duration
        )

        # Her bir cevabı kaydet
        for answer in answers:
            UserAnswer.objects.create(
                user=request.user,
                test_result=test_result,
                question_id=answer['question'],
                selected_choice_id=answer.get('selected_choice'),
                is_correct=answer['is_correct'],
                time_spent=answer.get('time_spent', 0)
            )

        return Response({'message': 'Test sonucu başarıyla kaydedildi.'}, 
                      status=status.HTTP_201_CREATED)

    @action(detail=False)
    def my_results(self, request):
        """
        Kullanıcının tüm test sonuçlarını listeler.
        """
        results = UserTestResult.objects.filter(user=request.user)
        serializer = UserTestResultSerializer(results, many=True)
        return Response(serializer.data)