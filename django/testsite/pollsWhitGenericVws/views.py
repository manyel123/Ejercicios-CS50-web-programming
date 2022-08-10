from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import F

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'pollsWhitGenericVws/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'pollsWhitGenericVws/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollsWhitGenericVws/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice'] returns the ID of the selected choice as a string
        # request.POST values are always strings.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    # The above code checks for KeyError and redisplays the question form with an error message if choice isn’t given
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'pollsWhitGenericVws/detail.html', {
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
        return HttpResponseRedirect(reverse('pollsWhitGenericVws:results', args=(question_id,)))