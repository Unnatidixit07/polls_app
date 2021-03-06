
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse
from django.db.models import F
from .models import Choice, Question
from django.template import loader


def index(request):
    latest_question_list = Question.objects.order_by('-date_pub')
    context = {
        'latest_question_list':latest_question_list,
    }
    return render(request, 'pollApp/index.html', context)

def detail(request, question_id):
    question= get_object_or_404(Question,pk=question_id)
    return render(request,'pollApp/detail.html',{'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'pollApp/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'pollApp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.vote = F('vote')+1
        selected_choice.save()
        return HttpResponseRedirect(reverse('poll_app:results', args=(question.id,)))