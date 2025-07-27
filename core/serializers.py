# core/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Subject, Topic, Question, Choice, Test, UserTestResult, UserAnswer

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            password=validated_data['password']
        )
        return user

class RagQuerySerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
    ders = serializers.CharField(max_length=100, required=False, default='Genel')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'date_joined')

# Test Modülü Serializers
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'difficulty', 'explanation', 'choices', 'topic']

class TopicSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'subject', 'questions_count']

    def get_questions_count(self, obj):
        return obj.questions.count()

class SubjectSerializer(serializers.ModelSerializer):
    topics_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'topics_count']

    def get_topics_count(self, obj):
        return obj.topics.count()

class TestListSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'type', 'created_by_username', 
                 'created_at', 'duration', 'is_public', 'questions_count']

    def get_questions_count(self, obj):
        return obj.questions.count()

class TestDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'type', 'created_by_username',
                 'created_at', 'duration', 'is_public', 'questions']

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['question', 'selected_choice', 'is_correct', 'time_spent']

class UserTestResultSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True, read_only=True)
    test_title = serializers.CharField(source='test.title', read_only=True)

    class Meta:
        model = UserTestResult
        fields = ['id', 'test', 'test_title', 'score', 'completed_at', 
                 'duration_taken', 'answers']