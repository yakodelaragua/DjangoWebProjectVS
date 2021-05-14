"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm,OrderFilter
from django.shortcuts import redirect
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    category_list = []
    for question in latest_question_list:
        if question.category_text not in category_list:
            category_list.append(question.category_text)
    
    
    template = loader.get_template('polls/index.html')

    myFilter = OrderFilter(request.GET, queryset=latest_question_list)
    latest_question_list = myFilter.qs
   
    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': latest_question_list,
                'category_list': category_list,
                'myFilter': myFilter,
   
              }
    return render(request, 'polls/index.html', context)



def detail(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def detaila(request, question_id, selected_choice):
    question = get_object_or_404(Question, pk=question_id)
    seleccionado = get_object_or_404(Choice, pk=selected_choice)

    if  seleccionado.correct_check:
        resultado='Correcto'
    else:
        resultado='Incorrecto'
        
    return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question, 'resultado': resultado})

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question})

def results(request, question_id, selected_choice):
  
    question = get_object_or_404(Question, pk=question_id)
    seleccionado = get_object_or_404(Choice, pk=selected_choice)

    if  seleccionado.correct_check:
        resultado='Correcto'
    else:
        resultado='Incorrecto'
   

    return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question, 'resultado': resultado})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('detail', args=(p.id, selected_choice.id)))

def votes(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id, selected_choice.id)))



def comprobarcorrecto(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    seleccionado = get_object_or_404(Choice, pk=selected_choice)

    if  seleccionado.correct_check:
        resultado='Correcto'
    else:
        resultado='Incorrecto'
      
    return HttpResponseRedirect(reverse('detail', args=(p.id, seleccionado.id)))



def viewvote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id, selected_choice.id)))


def question_new(request):
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.pub_date=datetime.now()
                question.question_num = 0
                question.save()
                estado = 'Pregunta correctamente añadida'
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = QuestionForm()
            estado = ''
        return render(request, 'polls/question_new.html', {'form': form, 'estado': estado,})


def choice_add(request, question_id):
        question = Question.objects.get(id = question_id)
        question_num = Choice.objects.filter(question = question_id).count()
        choices = Choice.objects.filter(question = question_id)
        estado = ''

        if request.method =='POST':
            form = ChoiceForm(request.POST)
            if form.is_valid():
                if question_num < 4:
                    has_marked_correct_check = form.cleaned_data['correct_check']
                    num_correct_choices = choices.filter(correct_check = True).count()

                    if num_correct_choices > 0 and has_marked_correct_check is True:
                        estado = 'Solo puede haber una respuesta correcta por pregunta'

                    else:
                        choice = form.save(commit = False)
                        choice.question = question
                        choice.vote = 0
                        choice.save()
                        estado = 'Respuesta correctamente añadida'
                        if question_num < 2:
                            estado = 'Respuesta correctamente añadida, introduce al menos dos opciones'

                else:
                    estado = 'Se ha alcanzado el límite de respuestas posibles'
      
        else: 
            form = ChoiceForm()
        #return render_to_response ('choice_new.html', {'form': form, 'poll_id': poll_id,}, context_instance = RequestContext(request),)
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.question_text,'form': form, 'estado': estado, 'choices': choices})

def chart(request, question_id):
    q=Question.objects.get(id = question_id)
    qs = Choice.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')

    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)

def show_categories(request):
    
    return render(request, 'polls/show_categories.html')