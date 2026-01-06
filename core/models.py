from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Расширенный пользователь"""
    ROLE_CHOICES = [
        ('parent', 'Родитель'),
        ('child', 'Ребёнок'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='parent')
    family = models.ForeignKey('Family', on_delete=models.CASCADE, null=True, blank=True)
    points = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

class Family(models.Model):
    """Семья"""
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def total_points(self):
        return sum(user.points for user in self.user_set.all())
    
    def __str__(self):
        return self.name

class AirQuality(models.Model):
    """Данные о воздухе"""
    district = models.CharField(max_length=100)  # Yunusabad, Chilanzar...
    aqi = models.IntegerField()  # Индекс качества воздуха
    date = models.DateField(auto_now_add=True)
    recommendation = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def get_status(self):
        if self.aqi <= 50:
            return 'Хорошо', 'success'
        elif self.aqi <= 100:
            return 'Средне', 'warning'
        else:
            return 'Плохо', 'danger'

class Quest(models.Model):
    """Квесты"""
    QUEST_TYPES = [
        ('light', 'Выключи свет'),
        ('plastic', 'Собери пластик'),
        ('plant', 'Полей растение'),
        ('transport', 'Используй общ. транспорт'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    quest_type = models.CharField(max_length=20, choices=QUEST_TYPES)
    points = models.IntegerField(default=10)
    for_role = models.CharField(max_length=10, default='child')  # child/parent/both
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class QuestCompletion(models.Model):
    """Выполненные квесты"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='quest_photos/', null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Родитель одобряет
    
    class Meta:
        ordering = ['-completed_at']

class Reward(models.Model):
    """Награды"""
    title = models.CharField(max_length=200)
    partner = models.CharField(max_length=200)  # Название партнёра
    discount = models.IntegerField()  # Процент скидки
    required_points = models.IntegerField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.discount}%"

class RewardRedemption(models.Model):
    """Получение награды"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=50)  # Промокод