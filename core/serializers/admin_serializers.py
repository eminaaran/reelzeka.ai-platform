from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

class ContentTypeSerializer(serializers.ModelSerializer):
    """ContentType modeli için serializer"""
    class Meta:
        model = ContentType
        fields = ['id', 'app_label', 'model']

class DynamicModelSerializer(serializers.ModelSerializer):
    """Dinamik model serializer temel sınıfı"""
    pass

class AdminActionSerializer(serializers.Serializer):
    """Admin işlemleri için serializer"""
    action = serializers.CharField()
    model = serializers.IntegerField()  # ContentType ID
    data = serializers.JSONField(required=False)
    id = serializers.IntegerField(required=False)  # Object ID for updates/deletes
