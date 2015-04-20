import re
from django import forms
from django.core.urlresolvers import reverse
from django.forms import DateTimeField, ChoiceField, CharField
from iq.tags.models import Tag
from iq.categories.models import Category
from .enums import QuestionOrderChoices
from .models import Question, CategoryQuestion


class QuestionSearchForm(forms.Form):
    """
    Search for and filter through a list of questions
    """
    order = ChoiceField(required=False, label="")
    tags = CharField(required=False, label="")

    def __init__(self, *args, **kwargs):
        requested_tags = kwargs.pop('requested_tags', None)
        super(QuestionSearchForm, self).__init__(*args, **kwargs)
        self.fields['tags'].initial = requested_tags
        self.fields['tags'].widget.attrs['placeholder'] = "To filter by tags, enter tags here separated by spaces"
        self.fields['order'].choices = QuestionOrderChoices

    def search(self):
        questions = Question.objects.all()
        if self.is_bound and self.is_valid() and self.cleaned_data.get("order"):
            if self.cleaned_data[ 'order' ] == str(QuestionOrderChoices.BODY):
                questions = questions.order_by('body')
            if self.cleaned_data['order'] == str(QuestionOrderChoices.CREATED_ON):
                questions = questions.order_by('-created_on')
            if self.cleaned_data['order'] == str(QuestionOrderChoices.CREATED_BY):
                questions = questions.order_by('created_by')
            if self.cleaned_data['order'] == str(QuestionOrderChoices.DIFFICULTY):
                questions = questions.order_by('difficulty')

        return questions


class QuestionForm(forms.ModelForm):
    """
    Form (based on Question model) for editing/creating questions
    """
    tags = forms.CharField(required=False, label="", widget=forms.widgets.HiddenInput)
    categories = forms.ModelMultipleChoiceField (
            queryset=Category.objects.all(),
            widget=forms.widgets.CheckboxSelectMultiple,
            required=False,
    )

    class Meta:
        model = Question
        fields = (
            'body',
            'answer',
            'difficulty',
        )

    def __init__(self, *args, **kwargs):
        category_id = kwargs.pop('category_id', None)
        created_by = kwargs.pop('created_by', None)
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.instance.created_by = created_by

        # Custom field attributes
        self.fields["answer"].required = False
        self.fields["difficulty"].label = ""
        self.fields["difficulty"].required = False
        self.fields["difficulty"].widget.attrs['placeholder'] = "Select a difficulty from 1-5"
        self.fields["tags"].widget.attrs['placeholder'] = "Enter tags separated by spaces  (ex. Python HTML CSS)"

        if category_id is not None:
            self.fields["categories"].initial = Category.objects.filter(pk=category_id)

        # If the question instance exists, associate categories with it
        if self.instance.pk is not None:
            cats = Category.objects.filter(categoryquestion__question=self.instance)
            self.fields["categories"].initial = cats

            # Order this question's tags in a comma separated list
            tags = self.instance.tags.all()
            self.fields["tags"].initial = ", ".join([str(tag) for tag in tags])

    def clean_difficulty(self):
        """
        Ensures difficulty is a value from 0-5
        """
        diff = self.cleaned_data['difficulty']
        if diff is not None:
            if diff > 5 or diff < 0:
                raise forms.ValidationError("Please enter a value from 1-5")
        return diff

    def clean_tags(self):
        """
        Clean associated tags
        """
        tags = self.cleaned_data['tags']
        tags = set(tag.strip() for tag in re.split(r"[,\s]+", tags))
        for tag in tags:
            if re.search("[^0-9A-Za-z]+", tag):
                raise forms.ValidationError("This tag is invalid: %s" % tag)
        return tags

    def save(self, *args, **kwargs):
        """
        Overridden save method to accomodate for
        tag and category associations
        """
        question = super(QuestionForm, self).save(*args, **kwargs)
        cats = []
        CategoryQuestion.objects.filter(question=self.instance).delete()
        for category in self.cleaned_data['categories']:
            cats.append(CategoryQuestion(category=category, question=self.instance))
        CategoryQuestion.objects.bulk_create(cats)

        # Retrieve tags, clear existing data
        tags = self.cleaned_data['tags']
        question.tags.clear()

        # Create new tags list from cleaned data (clean_tags)
        for tag in tags:
            try:
                tag = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                tag = Tag(name=tag)
                tag.color = tag.get_random_tag_colors()[0]
                tag.background_color = tag.get_random_tag_colors()[1]
                tag.save()
            question.tags.add(tag)
        return question
