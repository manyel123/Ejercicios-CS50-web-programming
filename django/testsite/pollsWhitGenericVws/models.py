import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # redefines str function to show question text when converted into string
    def __str__(self):
        return self.question_text

    # this decorator will display a diferent header for the method was_published_recently in the admin page
    # and it will change booleans into check or x icons and also will allow to order them by date
    @admin.display(
        boolean = True,
        ordering = 'pub_date',
        description = 'Published recently?',
    )

    # this method evaluates if a particular question was published recently or not
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # redefines str function to show choice text when converted into string
    def __str__(self):
        return self.choice_text