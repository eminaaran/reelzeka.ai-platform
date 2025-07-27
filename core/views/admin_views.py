from django.contrib.admin.sites import site
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.apps import apps
from core.serializers.admin_serializers import (
    ContentTypeSerializer,
    DynamicModelSerializer,
    AdminActionSerializer
)

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class AdminAPIViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def list(self, request):
        """Tüm yönetilebilir modelleri listele"""
        content_types = ContentType.objects.all()
        serializer = ContentTypeSerializer(content_types, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Belirli bir model için kayıtları getir"""
        try:
            content_type = ContentType.objects.get(pk=pk)
            model = content_type.model_class()
            
            # Model için dinamik serializer oluştur
            serializer_class = type(
                f"{model.__name__}Serializer",
                (DynamicModelSerializer,),
                {"Meta": type("Meta", (), {"model": model, "fields": "__all__"})}
            )
            
            queryset = model.objects.all()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data)
        except ContentType.DoesNotExist:
            return Response({"error": "Model bulunamadı"}, status=404)

    @action(detail=True, methods=['post'])
    def create_object(self, request, pk=None):
        """Yeni kayıt oluştur"""
        try:
            content_type = ContentType.objects.get(pk=pk)
            model = content_type.model_class()
            serializer_class = type(
                f"{model.__name__}Serializer",
                (DynamicModelSerializer,),
                {"Meta": type("Meta", (), {"model": model, "fields": "__all__"})}
            )
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except ContentType.DoesNotExist:
            return Response({"error": "Model bulunamadı"}, status=404)

    @action(detail=True, methods=['put'])
    def update_object(self, request, pk=None):
        """Kayıt güncelle"""
        try:
            content_type = ContentType.objects.get(pk=pk)
            model = content_type.model_class()
            obj = model.objects.get(pk=request.data.get('id'))
            serializer_class = type(
                f"{model.__name__}Serializer",
                (DynamicModelSerializer,),
                {"Meta": type("Meta", (), {"model": model, "fields": "__all__"})}
            )
            serializer = serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except (ContentType.DoesNotExist, model.DoesNotExist):
            return Response({"error": "Kayıt bulunamadı"}, status=404)

    @action(detail=True, methods=['delete'])
    def delete_object(self, request, pk=None):
        """Kayıt sil"""
        try:
            content_type = ContentType.objects.get(pk=pk)
            model = content_type.model_class()
            obj = model.objects.get(pk=request.data.get('id'))
            obj.delete()
            return Response(status=204)
        except (ContentType.DoesNotExist, model.DoesNotExist):
            return Response({"error": "Kayıt bulunamadı"}, status=404)

    @action(detail=True, methods=['get'])
    def model_metadata(self, request, pk=None):
        """Model metadata bilgilerini getir"""
        try:
            content_type = ContentType.objects.get(pk=pk)
            model = content_type.model_class()
            fields = []
            for field in model._meta.fields:
                field_info = {
                    'name': field.name,
                    'type': field.get_internal_type(),
                    'verbose_name': str(field.verbose_name),
                    'required': not field.blank,
                    'help_text': str(field.help_text),
                    'choices': [{'value': c[0], 'label': c[1]} for c in field.choices] if field.choices else None
                }
                fields.append(field_info)
            
            return Response({
                'app_label': model._meta.app_label,
                'model_name': model._meta.model_name,
                'verbose_name': str(model._meta.verbose_name),
                'verbose_name_plural': str(model._meta.verbose_name_plural),
                'fields': fields
            })
        except ContentType.DoesNotExist:
            return Response({"error": "Model bulunamadı"}, status=404)
