# Django views.py testing example
> Django docs offer a tutorial over testing but lack an example for testing the vote > view. I, never had done testing before, tackled it and came up with this.


## Requirements 
> What I use but it's not requiring anything python3 specific.

*Python 3.7.0
*Django 2.0.7

## Purpose
I wanted to put this up for anyone that is just getting throught the documentation and run into the "tests" section feeling dumbfounded. I avoided testing but given enough time, it proves to be worth it.


##### Urls.py
```
from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/results/vote/', views.vote, name='vote'),
]
```


##### views.py
```
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from .models import *


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
```


##### test_views.py

```
import datetime
from django.utils import timezone
from ..models import Question, Choice
from django.urls import reverse


def create_current_question(question_text, hours, minutes, seconds):
    time = timezone.now() + datetime.timedelta(hours=hours,
                                               minutes=minutes, seconds=seconds)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(question, choice_text):
    return Choice.objects.create(
        question=question,
        choice_text=choice_text,
        votes=0)


class QuestionVoteViewTests(TestCase):
    """
    This test will: vote on a choice attached to a question created -> by url 'polls:vote'. Then redirect to 'polls:results' displaying the question, choice and vote that has been incrimented.
    """

    def test_vote_view_with_voting(self):
        question = create_current_question(
            question_text="Does this test the vote view?",
            hours=23,
            minutes=59,
            seconds=59)
        choice = create_choice(
            question=question,
            choice_text="Choice for view question")
        url = reverse('polls:vote', kwargs={'question_id': choice.question.id})
        response = self.client.post(url, data={'choice': 1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Results of question %s" % question.id)
        self.assertRedirects(
            response,
            '/polls/1/results/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True)

    """
    This test will: Not vote on a choice attached to a question created --> by url 'polls:vote'. Fail, then direct back to 'detail.html' with error message "You forgot to select anything you idiot".
    """

    def test_vote_view_without_voting(self):
        question = create_current_question(
            question_text="Does this test the vote view?",
            hours=23,
            minutes=59,
            seconds=59)
        choice = create_choice(
            question=question,
            choice_text="Choice for view question")
        url = reverse('polls:vote', kwargs={'question_id': choice.question.id})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "You forgot to select anything you idiot")
```
