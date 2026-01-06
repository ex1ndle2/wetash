# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db import models
from .models import User, Family, AirQuality, Quest, QuestCompletion, Reward, RewardRedemption
from .forms import RegisterForm
from .utils import fetch_air_quality
import random
import string
# @login_required
def home(request):
    """Главная страница"""
    districts = ['Yunusabad', 'Chilanzar', 'Mirzo Ulugbek', 'Sergeli']
    air_data = AirQuality.objects.filter(district__in=districts)[:4]
    
    # Дополнительные данные для авторизованных пользователей
    completed_quests = 0
    if request.user.is_authenticated:
        completed_quests = QuestCompletion.objects.filter(user=request.user, approved=True).count()
    
    return render(request, 'home.html', {
        'air_data': air_data,
        'completed_quests': completed_quests
    })


def air_quality_view(request):
    """Страница качества воздуха"""
    districts = AirQuality.objects.values('district').distinct()
    selected = request.GET.get('district', 'Yunusabad')
    
    # Получаем данные с API (или из БД если недавно обновляли)
    air = AirQuality.objects.filter(district=selected).first()
    if not air:
        aqi = fetch_air_quality(selected)  # Функция в utils.py
        air = AirQuality.objects.create(district=selected, aqi=aqi)
    
    return render(request, 'air_quality.html', {
        'districts': districts,
        'selected': selected,
        'air': air
    })

# @login_required
def quests_view(request):
    """Страница квестов"""
    # Доступные квесты для текущего пользователя
    quests = Quest.objects.filter(
        is_active=True
    ).filter(
        models.Q(for_role=request.user.role) | models.Q(for_role='both')
    )
    
    # Выполненные квесты
    completed = QuestCompletion.objects.filter(user=request.user)
    
    return render(request, 'quests.html', {
        'quests': quests,
        'completed': completed
    })

# @login_required
def complete_quest(request, quest_id):
    """Выполнить квест"""
    quest = get_object_or_404(Quest, id=quest_id)
    
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        completion = QuestCompletion.objects.create(
            user=request.user,
            quest=quest,
            photo=photo,
            approved=(request.user.role == 'parent')  # Родители сами себя одобряют
        )
        
        if completion.approved:
            request.user.points += quest.points
            request.user.save()
        
        return redirect('quests')
    
    return render(request, 'complete_quest.html', {'quest': quest})

# @login_required
def approve_quest(request, completion_id):
    """Родитель одобряет квест ребёнка"""
    if request.user.role != 'parent':
        return redirect('quests')
    
    completion = get_object_or_404(QuestCompletion, id=completion_id)
    if completion.user.family == request.user.family and not completion.approved:
        completion.approved = True
        completion.save()
        
        completion.user.points += completion.quest.points
        completion.user.save()
    
    return redirect('family')

# @login_required
def family_view(request):
    """Семейная статистика"""
    family = request.user.family
    
    if not family:
        # Если у пользователя нет семьи, перенаправляем на главную
        return redirect('core:home')
    
    members = User.objects.filter(family=family).order_by('-points')
    
    # Ждут одобрения
    pending = QuestCompletion.objects.filter(
        user__family=family,
        approved=False
    )
    
    return render(request, 'family.html', {
        'family': family,
        'members': members,
        'pending': pending
    })

# @login_required
def rewards_view(request):
    """Награды"""
    rewards = Reward.objects.filter(is_active=True)
    my_rewards = RewardRedemption.objects.filter(user=request.user)
    
    return render(request, 'rewards.html', {
        'rewards': rewards,
        'my_rewards': my_rewards,
        'my_points': request.user.points
    })

# @login_required
def redeem_reward(request, reward_id):
    """Получить награду"""
    reward = get_object_or_404(Reward, id=reward_id)
    
    if request.method == 'POST' and request.user.points >= reward.required_points:
        request.user.points -= reward.required_points
        request.user.save()
        
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        RewardRedemption.objects.create(
            user=request.user,
            reward=reward,
            code=code
        )
    
    return redirect('rewards')

def register_view(request):
    """Регистрация"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def advice_list(request):
    return render(request, 'advice.html')

def game_view(request):
    return render(request, 'game.html')


def login_view(request):
    return render(request, 'registration/login.html')