import datetime
from http import client
from urllib import response
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

# Create your tests here.

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        t =timezone.now() + datetime.timedelta(days=30)
        future_quest = Question(pub_date=t)
        self.assertIs(future_quest.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        t = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_quest = Question(pub_date=t)
        self.assertIs(old_quest.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        t  = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_quest = Question(pub_date=t)
        self.assertIs(recent_quest.was_published_recently(), True)

def create_question(question_text, days):
    """
    creates a question with the given question_text and published 
    the given no of days offset to now (-ve for past questions and +ve for future(yet))
    """
    t =timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=t)

class LatestViewTest(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:latest"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerySetEqual(response.context['latest_question'], [])

    def test_future_questions(self):
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse("polls:latest"))
        self.assertContains(response, "No polls available")
        self.assertQuerySetEqual(response.context['latest_question'], [])

    def test_future_past_questions(self):
        create_question(question_text="Another Future", days=31)
        create_question(question_text="Past", days=-30)
        response = self.client.get(reverse('polls:latest'))
        self.assertQuerySetEqual(response.context['latest_question'], ['<Question: Past>'])


    def test_two_past_questions(self):
        create_question(question_text="Past Quest 1.", days=-30)
        create_question(question_text="Past Quest 2.", days=-5)
        response = self.client.get(reverse("polls:latest"))
        self.assertQuerySetEqual(response.context['latest_question'], ['<Question: Past Quest 2.>', '<Question: Past Quest 1.>'])