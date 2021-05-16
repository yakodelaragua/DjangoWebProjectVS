"""
Definition of models.
"""

from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Question(models.Model):
    level = (
            ('Facil', 'Facil'),
            ('Medio', 'Medio'),
            ('Dificil', 'Dificil'),
            )
    question_text = models.CharField(max_length=200, verbose_name="Pregunta")
    category_text = models.CharField(max_length=200, verbose_name="Categoría")
    pub_date = models.DateTimeField('date published')
    question_num = models.IntegerField(default='0')
    level = models.CharField(max_length=1000, null=True, choices=level, verbose_name="Dificultad")

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    correct_check = models.BooleanField()
    votes = models.IntegerField(default=0)

class User(models.Model):
    email = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)

