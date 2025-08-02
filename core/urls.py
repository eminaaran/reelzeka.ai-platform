# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.admin_views import AdminAPIViewSet
from .views.test_views import SubjectViewSet, TopicViewSet, TestViewSet
from .views.user_views import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    CheckAuthAPIView,
    get_csrf_token,
    UserListView
)
from django.urls import path
from .views.chat_views import ChatbotView # Yeni view'ı import et


# ViewSet'ler için router oluştur
router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'tests', TestViewSet, basename='test')
router.register(r'admin/models', AdminAPIViewSet, basename='admin-models')

urlpatterns = [
    # API endpoints
    path('register/', UserRegistrationAPIView.as_view(), name='api_register'),
    path('login/', UserLoginAPIView.as_view(), name='api_login'),
    path('logout/', UserLogoutAPIView.as_view(), name='api_logout'),
    path('check-auth/', CheckAuthAPIView.as_view(), name='api_check_auth'),
    path('csrf/', get_csrf_token, name='api_csrf'),
    path('admin/users/', UserListView.as_view(), name='api_admin_users'),
    path('chatbot-query/', ChatbotView.as_view(), name='chatbot-query'),

     

    # Test modülü URL'leri
    path('', include(router.urls)),
]