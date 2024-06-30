import random

from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Question, Answer, Game
from .forms import CustomLoginForm


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'auth/login.html', {'form': form})


@login_required
def start_game(request):
    questions = list(Question.objects.annotate(num_answers=Count('answers'))
                     .filter(num_answers__gte=2).order_by('?')[:5])

    game = Game.objects.create(player=request.user)
    game.questions.set(questions)
    game.save()

    return redirect('play_game', game_id=game.id)


@login_required
def play_game(request, game_id):
    game = Game.objects.get(id=game_id)

    if game.completed:
        return redirect('game_results', game_id=game.id)

    if game.current_question > 5:
        game.completed = True
        game.save()
        return redirect('game_results', game_id=game.id)

    question = game.questions.all()[game.current_question - 1]
    answers = list(question.answers.all())
    random.shuffle(answers)

    if request.method == 'POST':
        selected_answer_id = request.POST.get('answer')
        selected_answer = Answer.objects.get(id=selected_answer_id)

        if selected_answer.is_correct:
            game.score += question.points

        game.current_question += 1
        game.save()

        return render(request, 'answer_result.html', {
            'game': game,
            'question': question,
            'selected_answer': selected_answer,
            'correct_answer': question.answers.get(is_correct=True),
        })

    return render(request, 'play.html', {
        'game': game,
        'question': question,
        'answers': answers,
    })


@login_required
def game_result(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'result.html', {'game': game})
