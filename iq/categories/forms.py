from django import forms
from django.core.urlresolvers import reverse
from django.forms import DateTimeField, ChoiceField, CharField
from .models import Category
from iq.questions.models import Question, CategoryQuestion


class CategoryForm(forms.ModelForm):
    """
    Form (based on Category model) for editing a category
    """
    class Meta:
        model = Category
        fields = (
            'name',
            'description',
        )

    def __init__(self, *args, **kwargs):
        created_by = kwargs.pop('created_by', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.instance.created_by = created_by

        # Custom form attributes
        self.fields["name"].label = "Category Name"
        self.fields["description"].required = False
