from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_game, name='start_game'),
    path('play/<int:game_id>/<int:question_index>/',
         views.play_game, name='play_game'),
    path('results/<int:game_id>/', views.game_result, name='game_results'),
]
