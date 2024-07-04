"""
URL configuration for millionaire_game project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from game import views as game_views
from account import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', game_views.home, name='home'),
    path('game/', include('game.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', account_views.register, name='register'),
    path('login/', account_views.custom_login, name='login'),
    path('logout/', account_views.custom_logout, name='logout'),
    path('leaderboard/', account_views.leaderboard, name='leaderboard'),
]
