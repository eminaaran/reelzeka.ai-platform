# core/urls.py
from django.urls import path
from .views import (
    RagQueryAPIView,
    UserRegistrationAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    CheckAuthAPIView,
    get_csrf_token,
    UserListView # Yeni view'ı import et
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='api_register'),
    path('login/', UserLoginAPIView.as_view(), name='api_login'),
    path('logout/', UserLogoutAPIView.as_view(), name='api_logout'),
    path('check-auth/', CheckAuthAPIView.as_view(), name='api_check_auth'),
    path('csrf/', get_csrf_token, name='api_csrf'),
    path('rag-query/', RagQueryAPIView.as_view(), name='api_rag_query'),

    # Admin panel URL'leri
    path('admin/users/', UserListView.as_view(), name='api_admin_users'), # /api/admin/users/ olacak şekilde güncellendi
]