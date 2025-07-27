from rest_framework import serializers
from ..models import Subject, Topic, Test, Question, Choice, TestQuestion, UserTestResult

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    options = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'options']

class TestListSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'type', 'duration', 'question_count']

    def get_question_count(self, obj):
        return obj.questions.all().count()

class TestDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'type', 'duration', 'questions']

    def get_questions(self, obj):
        test_questions = TestQuestion.objects.filter(test=obj).order_by('order')
        return [{
            'id': tq.question.id,
            'text': tq.question.text,
            'options': [{'id': choice.id, 'text': choice.text} for choice in tq.question.choices.all()]
        } for tq in test_questions]

class TestSubmissionSerializer(serializers.Serializer):
    answers = serializers.DictField(child=serializers.CharField())
    duration_taken = serializers.IntegerField(required=False, default=0)

class TestResultSerializer(serializers.ModelSerializer):
    total_questions = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()

    class Meta:
        model = UserTestResult
        fields = ['score', 'total_questions', 'correct_answers', 'duration_taken']

    def get_total_questions(self, obj):
        return obj.test.questions.all().count()

    def get_correct_answers(self, obj):
        return int((obj.score / 100) * self.get_total_questions(obj))
