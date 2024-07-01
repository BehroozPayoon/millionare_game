from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from account.models import CustomUser


class Question(models.Model):
    text = models.CharField(max_length=255)
    points = models.PositiveIntegerField(
        validators=[MinValueValidator(5),
                    MaxValueValidator(20)]
    )

    def __repr__(self) -> str:
        return f"<Question {self.text}>"

    def __str__(self) -> str:
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __repr__(self) -> str:
        return f"<Answer {self.text}>"

    def __str__(self) -> str:
        return self.text


class Game(models.Model):
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    current_question = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return f"Game for {self.player.email}"
