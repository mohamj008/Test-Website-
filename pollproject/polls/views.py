from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, "polls/index.html")



class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"
    context_object_name = "q_details"
    

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    context_object_name = 'questn'

class LatestView(generic.ListView):
    model = Question
    template_name = "polls/lists.html"
    context_object_name = 'latest_question'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

def vote(request, question_id):
    quest = get_object_or_404(Question, pk=question_id)
    try:
        selectchoice = quest.choice_set.get(pk=request.POST['choice']) 
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/polls.html', {'quest': quest, 'error_message': 'no choice selected'})
    
    else:
        selectchoice.votes += 1
        selectchoice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(quest.id,)))

    return render(request, "polls/polls.html")
