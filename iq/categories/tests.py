import datetime
from unittest import TestCase, mock
from unittest.mock import patch
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from model_mommy.mommy import make, prepare
from iq.questions.models import Question, CategoryQuestion
from iq.categories.models import Category
from iq.categories.forms import CategoryForm
from iq.utils.tests import IqCustomTest


class CategoryModelsTest(IqCustomTest):
    """
    Tests category models for appropriate data
    """
    def setUp(self):
        super(CategoryModelsTest, self).setUp()

    def test_category_model(self):
        c = make(Category)
        self.assertEquals(c.name, c.__str__())


class CategoryFormsTest(IqCustomTest):
    """
    Tests and ensure form validation and invalidation
    functions properly
    """
    def setUp(self):
        super(CategoryFormsTest, self).setUp()

    def test_valid_category_form(self):
        form = CategoryForm(created_by=self.user, data={
            "name": "Valid Category",
            "description": "is a new category",
        })
        self.assertTrue(form.is_valid())
        new_category = form.save()
        self.assertEqual(new_category.created_by, self.user)
        self.assertEqual(form.fields["name"].label, "Category Name")
        self.assertFalse(form.fields["description"].required)


class CategoryViewsTest(IqCustomTest):
    """
    Tests and ensures the views return correct responses, and redirect
    to the appropriate pages.
    """
    def setUp(self):
        super(CategoryViewsTest, self).setUp()
        self.client.login(username=self.user.username, password="foo")
        self.question = make(Question)
        make(CategoryQuestion, question=self.question, category=self.category)

    def test_valid_list_get_view(self):
        response = self.client.get(reverse('categories-list'))
        self.assertEqual(response.status_code, 200)

    def test_valid_list_post_view(self):
        response = self.client.post(reverse('categories-list'))
        self.assertEqual(response.status_code, 200)

    def test_valid_detail_get_view(self):
        response = self.client.get(reverse('categories-detail', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)

    def test_valid_detail_post_view(self):
        response = self.client.post(reverse('categories-detail', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)

    def test_valid_printout_get_view(self):
        response = self.client.get(reverse('categories-printout', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)

    def test_valid_printout_post_view(self):
        response = self.client.post(reverse('categories-printout', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)

    def test_valid_printout_applicant_get_view(self):
        response = self.client.get(reverse('categories-printout_applicant', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)

    def test_valid_printout_applicant_post_view(self):
        response = self.client.post(reverse('categories-printout_applicant', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)

    def test_valid_create_get_view(self):
        response = self.client.get(reverse('categories-create'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_create_post_view(self):
        with patch('iq.categories.forms.CategoryForm.is_valid', return_value=False):
            response = self.client.post(reverse('categories-create'), data={"name": "invalid"})
        self.assertEqual(response.status_code, 200)

    def test_valid_create_post_view(self):
        with patch('iq.categories.forms.CategoryForm.is_valid', return_value=True):
            with patch('iq.categories.forms.CategoryForm.save', return_value=True):
                response = self.client.post(reverse('categories-create'), data={"name": "valid"})
        self.assertEqual(response.status_code, 302)

    def test_valid_edit_get_view(self):
        response = self.client.get(reverse('categories-edit', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)

    def test_invalid_edit_post_view(self):
        with patch('iq.categories.forms.CategoryForm.is_valid', return_value=False):
            response = self.client.post(reverse('categories-edit',
                args=[self.category.pk]),
                    data={"name": "invalid"}
            )
        self.assertEqual(response.status_code, 200)

    def test_valid_edit_post_view(self):
        with patch('iq.categories.forms.CategoryForm.is_valid', return_value=True):
            with patch('iq.categories.forms.CategoryForm.save', return_value=True):
                response = self.client.post(reverse('categories-edit',
                    args=[self.category.pk]),
                        data={"name": "valid"}
                )
        self.assertEqual(response.status_code, 302)

    def test_valid_delete_get_view(self):
        response = self.client.get(reverse('categories-delete', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)

    def test_valid_delete_post_view(self):
        response = self.client.post(reverse('categories-delete', args=[self.category.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('categories-list'))
