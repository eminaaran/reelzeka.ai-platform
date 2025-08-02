from django.db import models
from django.contrib.auth.models import User

class Belge(models.Model):
    ders_adi = models.CharField(max_length=100, help_text="Örn: Edebiyat, Tarih")
    dosya = models.FileField(upload_to='belgeler/', help_text=".txt uzantılı olmalı")
    yuklenme_tarihi = models.DateTimeField(auto_now_add=True)
    indekslendi_mi = models.BooleanField(default=False, help_text="Bu dosya RAG veritabanına eklendi mi?")

    def __str__(self):
        dosya_adi = self.dosya.name.split('/')[-1]
        return f"{self.ders_adi} - {dosya_adi}"

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.prompt[:50]}'

# Test Modülü Modelleri
class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Kolay'),
        ('medium', 'Orta'),
        ('hard', 'Zor'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Onay Bekliyor'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.topic.name} - {self.text[:50]}..."

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Test(models.Model):
    TEST_TYPES = [
        ('practice', 'Alıştırma Testi'),
        ('mock', 'Deneme Sınavı'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TEST_TYPES, default='practice')
    questions = models.ManyToManyField(Question, through='TestQuestion')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(help_text="Test süresi (dakika)", default=40)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)
    duration_taken = models.IntegerField(help_text="Geçirilen süre (saniye)")
    
    class Meta:
        unique_together = ['user', 'test']

    def __str__(self):
        return f"{self.user.username} - {self.test.title}: {self.score}"

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_result = models.ForeignKey(UserTestResult, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    time_spent = models.IntegerField(help_text="Soruda geçirilen süre (saniye)", default=0)

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}"