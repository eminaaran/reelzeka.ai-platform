# core/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, generics
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import os
from dotenv import load_dotenv 
import google.generativeai as genai
from rest_framework.permissions import IsAuthenticated

# Serializer'lar
from .serializers import (
    UserRegistrationSerializer, RagQuerySerializer, UserSerializer,
    SubjectSerializer, TopicSerializer, QuestionSerializer,
    TestListSerializer, TestDetailSerializer, UserTestResultSerializer
)
from .models import Subject, Topic, Question, Test, UserTestResult, UserAnswer

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# Gemini modelini yapılandır
try:
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY bulunamadı.")
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"!!! GEMINI YAPILANDIRMA HATASI: {e}")
    model = None

# --- GÜVENLİK VE KİMLİK DOĞRULAMA VIEWS ---

@ensure_csrf_cookie
def get_csrf_token(request):
    """Frontend'in CSRF cookie'sini almasını sağlayan view."""
    return JsonResponse({"detail": "CSRF cookie set"})

class UserRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
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
    def post(self, request):
        logout(request)
        return Response({"success": "Başarıyla çıkış yapıldı"}, status=status.HTTP_200_OK)

class CheckAuthAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        return Response({"error": "Giriş yapılmamış"}, status=status.HTTP_401_UNAUTHORIZED)


# --- TEST MODÜLÜ VIEWS ---

class TestViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Test.objects.all()
        return Test.objects.filter(is_public=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return TestListSerializer
        return TestDetailSerializer

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        test = self.get_object()
        answers = request.data.get('answers', [])
        duration = request.data.get('duration')
        score = request.data.get('score')

        test_result = UserTestResult.objects.create(
            user=request.user, test=test, score=score, duration_taken=duration
        )

        for answer in answers:
            UserAnswer.objects.create(
                user=request.user, test_result=test_result,
                question_id=answer['question'],
                selected_choice_id=answer.get('selected_choice'),
                is_correct=answer['is_correct'],
                time_spent=answer.get('time_spent', 0)
            )
        return Response({'message': 'Test sonucu başarıyla kaydedildi.'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def my_results(self, request):
        results = UserTestResult.objects.filter(user=request.user)
        serializer = UserTestResultSerializer(results, many=True)
        return Response(serializer.data)

# --- ADMIN PANELİ VIEWS ---

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# Diğer admin view'leri buraya eklenebilir...
