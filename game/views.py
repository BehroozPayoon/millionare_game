from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from .models import Question, Answer, Game


def home(request):
    return render(request, 'home.html')


@login_required
def start_game(request):
    questions = list(Question.objects.annotate(num_answers=Count('answers'))
                     .filter(num_answers__gte=2).order_by('?')[:5])

    game = Game.objects.create(player=request.user)
    game.questions.set(questions)
    game.save()

    return redirect('play_game', game_id=game.id, question_index=1)


@login_required
def play_game(request, game_id, question_index):
    game = Game.objects.get(id=game_id)

    if game.completed:
        return redirect('game_results', game_id=game.id)

    if game.current_question > 5:
        game.completed = True
        game.save()
        return redirect('game_results', game_id=game.id)

    question = game.questions.all()[question_index - 1]
    answers = list(question.answers.all())

    if request.method == 'POST':
        return _process_answer(request.POST, question, question_index,
                               game, request)

    return render(request, 'play.html', {
        'game': game,
        'question': question,
        'answers': answers,
    })


def _process_answer(post_data, question, question_index,
                    game, request):

    selected_answer_id = post_data.get('answer')
    selected_answer = Answer.objects.get(id=selected_answer_id)
    correct_answer = question.answers.get(is_correct=True)

    if question_index >= game.current_question:
        if selected_answer.is_correct:
            game.score += question.points

        game.current_question += 1
        game.save()

    return render(request, 'answer_result.html', {
        'game': game,
        'question': question,
        'selected_answer': selected_answer,
        'correct_answer': correct_answer,
        'question_index': question_index,
    })


@login_required
def game_result(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'result.html', {'game': game})
