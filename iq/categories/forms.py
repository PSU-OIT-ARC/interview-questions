from django import forms
from django.core.urlresolvers import reverse
from django.forms import DateTimeField, ChoiceField, CharField
from .models import Category
from iq.questions.models import Question, CategoryQuestion


class CategoryForm(forms.ModelForm):
    """
    Form (based on Category model) for editing a category
    """
    questions = forms.ModelMultipleChoiceField (
            queryset=Question.objects.all(),
            widget=forms.widgets.CheckboxSelectMultiple,
            required=False,
    )

    class Meta:
        model = Category
        fields = (
            'name',
            'description',
            'color',
            'background_color',
        )

    def __init__(self, *args, **kwargs):
        created_by = kwargs.pop('created_by', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.instance.created_by = created_by

        # Custom form attributes
        self.fields["name"].label = "Category Name"
        self.fields["description"].required = False
        self.fields["color"].required = False
        self.fields["color"].widget.attrs['placeholder'] ="Enter a font color (hex)"
        self.fields["background_color"].required = False
        self.fields["background_color"].widget.attrs['placeholder'] = "Enter a background color (hex)"

        if self.instance.pk is not None:
            qs = Question.objects.filter(categoryquestion__category=self.instance)
            self.fields['questions'].initial = qs

    def save(self, *args, **kwargs):
        """
        Override save method for questions field
        """
        category = super(CategoryForm, self).save(*args, **kwargs)

        #category = super(CategoryForm, self)
        #category.color = category.get_random_cat_colors()[0]
        #category.background_color = category.get_random_cat_colors()[1]
        #category.save()

        # delete all the questions this category is a part
        # of, and then re-add them
        CategoryQuestion.objects.filter(category=self.instance).delete()
        qs = []
        for question in self.cleaned_data['questions']:
            qs.append(CategoryQuestion(category=self.instance, question=question))
        CategoryQuestion.objects.bulk_create(qs)

        return category
