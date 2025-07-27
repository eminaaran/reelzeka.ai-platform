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
from .views.rag_views import RagQueryAPIView

# ViewSet'ler için router oluştur
router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'tests', TestViewSet, basename='test')
router.register(r'admin/models', AdminAPIViewSet, basename='admin-models')

urlpatterns = [
    # API endpoints
    path('api/register/', UserRegistrationAPIView.as_view(), name='api_register'),
    path('api/login/', UserLoginAPIView.as_view(), name='api_login'),
    path('api/logout/', UserLogoutAPIView.as_view(), name='api_logout'),
    path('api/check-auth/', CheckAuthAPIView.as_view(), name='api_check_auth'),
    path('api/csrf/', get_csrf_token, name='api_csrf'),
    path('api/rag-query/', RagQueryAPIView.as_view(), name='api_rag_query'),
    path('api/admin/users/', UserListView.as_view(), name='api_admin_users'),

    # Test modülü URL'leri
    path('api/', include(router.urls)),
]