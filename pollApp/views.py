
from django.shortcuts import get_object_or_404, render, redirect
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

def insert(request):
    if request.method=='POST':
       _question = request.POST['_question']
       choice_one = request.POST["choice_one"]
       choice_two = request.POST["choice_two"]
       choice_three = request.POST["choice_three"]
       choice_four = request.POST["choice_four"]
       choice_five = request.POST["choice_five"]
       question_added=Question.objects.create(question_asked=_question)
       Choice.objects.create(choice_made=choice_one, question=question_added)
       Choice.objects.create(choice_made=choice_two, question=question_added)
       if choice_three:
          Choice.objects.create(choice_made=choice_three, question=question_added)
       if choice_four:   
          Choice.objects.create(choice_made=choice_four, question=question_added)
       if choice_five:
          Choice.objects.create(choice_made=choice_five, question=question_added)
       return redirect( 'poll_app:index')
    return render(request, 'pollApp/insert.html')        