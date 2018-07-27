from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from django.views import generic
from django.utils import timezone

from .models import *

# ......

def vote(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = req.POST['choice']
        selected_choice = question.choice_set.get(pk=choice)
    except (KeyError, Choice.DoesNotExist):
        error_message = "You forgot to select anything you idiot"
        return render(req, 'polls/detail.html', {
            'question': question,
            'error_message': error_message,
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return redirect(
            reverse(
                'polls:results',
                kwargs={
                    'question_id': question_id}))
