from django.test import TestCase

import datetime
from django.utils import timezone
from ..models import Question, Choice
from django.urls import reverse


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


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
