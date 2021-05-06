"""
Definition of models.
"""

from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    category_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.category_text

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    correct_check = models.BooleanField()
    votes = models.IntegerField(default=0)

class User(models.Model):
    email = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)

class Order(models.Model):
    question = models.ForeignKey(Question)
    
    def __str__(self):
        self.question.category_text
    