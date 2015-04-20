import datetime
from unittest import TestCase, mock
from unittest.mock import patch
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from model_mommy.mommy import make, prepare
from iq.questions.models import Question, CategoryQuestion
from iq.questions.forms import QuestionSearchForm, QuestionForm
from iq.questions.enums import QuestionOrderChoices
from iq.categories.models import Category
from iq.tags.models import Tag
from iq.utils.tests import IqCustomTest


class QuestionModelsTest(IqCustomTest):
    """
    Tests models in the Question app
    """
    def setUp(self):
        super(QuestionModelsTest, self).setUp()

    def test_question_model(self):
        q = Question (
            body = "testing question model body",
            answer = "testing question model answer",
            difficulty = 1,
            created_on = timezone.now(),
            created_by = self.user,
        )
        q.save()
        self.assertTrue(q)

    def test_categoryquestion_model(self):
        self.question = make(Question)
        cq = CategoryQuestion (
            question = self.question,
            category = self.category,
            created_on = timezone.now(),
            created_by = self.user,
        )
        cq.save()
        self.assertEqual(cq.question.pk, self.question.pk)
        self.assertEqual(cq.category.pk, self.category.pk)


class QuestionFormsTest(IqCustomTest):
    """
    Tests and ensure form validation and invalidation
    functions properly
    """
    def setUp(self):
        super(QuestionFormsTest, self).setUp()
        self.client.login(username=self.user.username, password="foo")

    def test_valid_question_form(self):
        form = QuestionForm(created_by=self.user, data={
            "body": "asdf",
            "answer": "fdsa",
            "difficulty": "5",
            "tags": "asdf,fdsa,asdfasdf"
        })
        form.is_valid()
        count = Question.objects.count()
        form.save()
        self.assertEqual(count+1, Question.objects.count())

    def test_valid_question_form_with_category(self):
        count = Question.objects.count()
        question = make(Question)
        form = QuestionForm(category_id=self.category.pk, instance=question, data={
            "body": "foo",
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(count+1, Question.objects.count())

    def test_invalid_question_form(self):
        form = QuestionForm(data={
            "body": "bad",
            "difficulty": "6",
            "tags": "<<>>//\\"
        })
        self.assertFalse(form.is_valid())

    def test_valid_search_form(self):
        choices = [
            QuestionOrderChoices.BODY,
            QuestionOrderChoices.CREATED_ON,
            QuestionOrderChoices.CREATED_BY,
            QuestionOrderChoices.DIFFICULTY,
        ]
        filter = [
            "body",
            "-created_on",
            "created_by",
            "difficulty"
        ]
        make(Question, _quantity=3)
        for i, j in zip(choices, filter):
            s = QuestionSearchForm(data={
                "order": i,
            })
            s.is_valid()
            results = s.search()
            actual  = Question.objects.order_by(j).first()
            self.assertEqual(results.first().body, actual.body)


class QuestionViewsTest(IqCustomTest):
    """
    Tests and ensures views return correct responses, and redirect
    to the appropriate pages.
    """
    def setUp(self):
        super(QuestionViewsTest, self).setUp()
        self.client.login(username=self.user.username, password="foo")
        self.question = make(Question)

    def test_valid_list_get_view(self):
        response = self.client.get(reverse('questions-list')
                + "?order=" + str(QuestionOrderChoices.CREATED_ON)
        )
        self.assertEqual(response.status_code, 200)

    def test_valid_list_post_view(self):
        response = self.client.post(reverse('questions-list'))
        self.assertEqual(response.status_code, 200)

    def test_valid_create_get_view(self):
        response = self.client.get(reverse('questions-create'))
        self.assertEqual(response.status_code, 200)

    def test_valid_create_post_view(self):
        with patch('iq.questions.forms.QuestionForm.is_valid', return_value=True):
            with patch('iq.questions.forms.QuestionForm.save', return_value=True):
                response = self.client.post(reverse('questions-create'), data={"body": "valid"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('questions-list'))

    def test_valid_create_post_with_category(self):
        with patch('iq.questions.forms.QuestionForm.is_valid', return_value=True):
            with patch('iq.questions.forms.QuestionForm.save', return_value=True):
                response = self.client.post(reverse('questions-create')
                    + "?category_id=" + str(self.category.pk),
                        data={"body": "appended to category"}
                )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('categories-detail', args=[self.category.pk]))

    def test_invalid_create_post_view(self):
        with patch('iq.questions.forms.QuestionForm.is_valid', return_value=False):
            response = self.client.post(reverse('questions-create'), data={"body": "invalid"})
        self.assertEqual(response.status_code, 200)

    def test_valid_edit_get_view(self):
        response = self.client.get(reverse('questions-edit', args=[self.question.pk]))
        self.assertEqual(response.status_code, 200)

    def test_valid_edit_post_view(self):
        with patch('iq.questions.forms.QuestionForm.is_valid', return_value=True):
            with patch('iq.questions.forms.QuestionForm.save', return_value=True):
                response = self.client.post(reverse('questions-edit',
                    args=[self.question.pk]),
                        data={"body": "valid"}
                )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('questions-list'))

    def test_valid_edit_post_with_category(self):
        with patch('iq.questions.forms.QuestionForm.is_valid', return_value=True):
            with patch('iq.questions.forms.QuestionForm.save', return_value=True):
                response = self.client.post(reverse('questions-edit',
                    args=[self.question.pk])
                    + "?category_id=" + str(self.category.pk),
                        data={"body": "edited within category"}
                )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('categories-detail', args=[self.category.pk]))

    def test_invalid_edit_post_view(self):
        with patch('iq.questions.forms.QuestionForm.is_valid', return_value=False):
            response = self.client.post(reverse('questions-edit',
                args=[self.question.pk]),
                    data={"body": "invalid"}
            )
        self.assertEqual(response.status_code, 200)

    def test_valid_delete_get_view(self):
        response = self.client.get(reverse('questions-delete', args=[self.question.pk]))
        self.assertEqual(response.status_code, 200)

    def test_valid_delete_post_view(self):
        response = self.client.post(reverse('questions-delete', args=[self.question.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/questions/list')

    def test_valid_delete_post_with_category(self):
        response = self.client.post(reverse('questions-delete', args=[self.question.pk])
                + "?category_id=" + str(self.category.pk)
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('categories-detail', args=[self.category.pk]))
