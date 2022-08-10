from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect


from .models import Choice, Question

def index(request):
    # getting all objects from question model as a list, then order by date and get the last 5
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # the context is a dictionary mapping TEMPLATE VARIABLE names to python objects
    context = {'latest_question_list':latest_question_list,}

    ''' the render function takes the request object as first argument, a template name as 
    second argument and a dictionary as its optional third argument  '''
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # get_object_or_404 sustituye al try except raise
    question = get_object_or_404(Question, pk=question_id)

    # como tercer argumento se pasa el diccionario del context directamente a la función render
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice'] returns the ID of the selected choice as a string
        # request.POST values are always strings.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    # The above code checks for KeyError and redisplays the question form with an error message if choice isn’t given
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # F() allows to separated users to vote at the same time without losing one the votes
        selected_choice.votes = F('votes') + 1
        selected_choice.save()

        # refresh_from_db() avoid the persistence caused by F() reloading the model object after saving it
        question.refresh_from_db()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})