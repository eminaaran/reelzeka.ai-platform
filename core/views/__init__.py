from .admin_views import AdminAPIViewSet
from .test_views import SubjectViewSet, TopicViewSet, TestViewSet
from .user_views import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    CheckAuthAPIView,
    get_csrf_token,
    UserListView
)
from .rag_views import RagQueryAPIView

__all__ = [
    'AdminAPIViewSet',
    'SubjectViewSet',
    'TopicViewSet',
    'TestViewSet',
    'UserRegistrationAPIView',
    'UserLoginAPIView',
    'UserLogoutAPIView',
    'CheckAuthAPIView',
    'get_csrf_token',
    'UserListView',
    'RagQueryAPIView'
]

# CSRF token view
@ensure_csrf_cookie
def get_csrf_token(request):
    """React'in CSRF cookie'sini almasını sağlayan basit view."""
    return JsonResponse({"detail": "CSRF cookie set"})

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

class RagQueryAPIView(APIView):
    def post(self, request):
        from ..serializers import RagQuerySerializer
        serializer = RagQuerySerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data.get('question')
            ders = serializer.validated_data.get('ders')
            try:
                from ..calistir import rag_ile_cevap_ver
                answer = rag_ile_cevap_ver(kullanici_sorusu=question, ders_adi=ders)
                return Response({"answer": answer})
            except Exception as e:
                return Response({"error": f"RAG sisteminde hata: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        users = User.objects.all().order_by('-date_joined')
        from ..serializers import UserSerializer
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
