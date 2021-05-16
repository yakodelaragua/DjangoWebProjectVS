"""
Definition of forms.
"""

from django import forms
from app.models import Question,Choice,User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import django_filters
from django_filters import DateFilter, CharFilter

class QuestionForm(forms.ModelForm):

        class Meta:
            model = Question
            fields = ('question_text', 'category_text', 'level',)

class ChoiceForm(forms.ModelForm):

        class Meta:
            model = Choice
            fields = ('choice_text', 'correct_check',)

class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('email','nombre',)

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="pub_date", lookup_expr='gte', label='A partir de (dd/mm/yyyy)')
    end_date = DateFilter(field_name="pub_date", lookup_expr='lte', label='Antes de (dd/mm/yyyy)')
    question = CharFilter(field_name='question_text', lookup_expr='icontains', label='Pregunta')

    class Meta:
        model = Question
        fields = ('category_text', 'level',)
        exclude = ('question_text', 'pub_date', 'question_num')