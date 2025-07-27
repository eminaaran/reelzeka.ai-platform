from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.user_serializers import UserSerializer, UserRegistrationSerializer

@ensure_csrf_cookie
def get_csrf_token(request):
    try:
        return JsonResponse({"detail": "CSRF cookie set"})
    except Exception as e:
        print("CSRF token hatası:", str(e))
        return JsonResponse({"error": str(e)}, status=500)

class UserRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        from ..serializers import UserRegistrationSerializer, UserSerializer
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
            from ..serializers import UserSerializer
            return Response(UserSerializer(user).data)
        return Response({"error": "Geçersiz kullanıcı adı veya şifre"}, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"success": "Başarıyla çıkış yapıldı"}, status=status.HTTP_200_OK)

class CheckAuthAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            from ..serializers import UserSerializer
            return Response(UserSerializer(request.user).data)
        return Response({"error": "Giriş yapılmamış"}, status=status.HTTP_401_UNAUTHORIZED)

class UserListView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        users = User.objects.all().order_by('-date_joined')
        from ..serializers import UserSerializer
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
