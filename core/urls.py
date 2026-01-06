from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'core'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # Аутентификация
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Качество воздуха
    path('air/', views.air_quality_view, name='air_quality'),
    
    # Квесты
    path('quests/', views.quests_view, name='quests'),
    path('quests/complete/<int:quest_id>/', views.complete_quest, name='complete_quest'),
    path('quests/approve/<int:completion_id>/', views.approve_quest, name='approve_quest'),
    
    # Семья
    path('family/', views.family_view, name='family'),
    
    # Награды
    path('rewards/', views.rewards_view, name='rewards'),
    path('rewards/redeem/<int:reward_id>/', views.redeem_reward, name='redeem_reward'),
    path('advice/', views.advice_list, name='advice'),
    path('game/', views.game_view, name='game'),
]
