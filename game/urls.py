from django.urls import path
from . import views

urlpatterns = [
    path('play/', views.play, name='play'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('signup/', views.signup, name='signup'),
]
