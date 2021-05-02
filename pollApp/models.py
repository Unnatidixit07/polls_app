import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    def __str__(self):
        return self.question_asked
    question_asked = models.CharField(max_length=250)
    date_pub = models.DateTimeField(auto_now_add=True)
    def was_published_recently(self):
        return self.date_pub >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    def __str__(self):
        return self.choice_made
    question_asked = models.ForeignKey(Question, on_delete=models.CASCADE) 
    choice_made = models.CharField(max_length=150)
    vote = models.IntegerField(default=0)

