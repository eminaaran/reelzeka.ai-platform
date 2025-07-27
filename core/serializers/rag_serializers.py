from rest_framework import serializers

class RagQuerySerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
    ders = serializers.CharField(max_length=100)
