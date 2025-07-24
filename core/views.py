# core/views.py (NİHAİ VE TAM HALİ)

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# Serializer'ları import etmemiz gerekiyor
from .serializers import UserRegistrationSerializer, RagQuerySerializer, UserSerializer

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
    # Varsayılan izin (IsAuthenticated) geçerli olacak, sadece giriş yapanlar soru sorabilir.
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