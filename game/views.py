import random

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Question, GameSession, UserProfile
# Create your views here.


@login_required
def play(request):
    if request.method == 'POST':
        score = _calculate_score(request.POST)
        GameSession.objects.create(user=request.user, score=score)

        # Update user's best score
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if score > profile.best_score:
            profile.best_score = score
            profile.save()
    else:
        questions = list(Question.objects.all())
        game_questions = random.sample(questions, min(5, len(questions)))
        return render(request, 'game/play.html', {'questions': game_questions})


def leaderboard(request):
    top_users = UserProfile.objects.order_by('-best_score')[:10]
    return render(request, 'game/leaderboard.html', {'top_users': top_users})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('play_game')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def _calculate_score(post_data):
    score = 0
    for key, value in post_data.items():
        if key.startswith('question_'):
            question_id = int(key.split('_')[1])
            question = Question.objects.get(id=question_id)
            correct_answer = question.answers.get(is_correct=True)
            if int(value) == correct_answer.id:
                score += question.points
    return score
