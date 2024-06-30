from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


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


class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    best_score = models.IntegerField(default=0)
