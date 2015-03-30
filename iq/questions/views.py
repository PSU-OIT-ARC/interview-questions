import datetime
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from iq.categories.models import Category
from iq.tags.models import Tag
from .forms import QuestionForm, QuestionSearchForm
from .models import Question, CategoryQuestion


"""
TODO: Work on better documentation
"""


def list_(request):
    """
    Display, search, and filter all questions
    Based off of MLP list_ view
    """
    if request.GET:
        form = QuestionSearchForm(request.GET)
    else:
        form = QuestionSearchForm()

    return render(request, 'questions/list.html', {
        "question_list": form.search(),
        "form": form,
    })


def detail(request, question_id):
    """
    Lists details of a single question
    """
    question = get_object_or_404(Question, pk=question_id)
    categories_assigned = Category.objects.filter(categoryquestion__question=question)

    return render(request, 'questions/detail.html', {
        "question": question,
        "categories_assigned": categories_assigned,
        "tags": question.tags.all(),
    })

def create(request):
    """
    Create a single question
    """
    return _edit(request, question_id=None)


def edit(request, question_id):
    """
    Edit an existing question
    """
    return _edit(request, question_id)


def _edit(request, question_id):
    """
    Edit a single question and it's attributes
    Some serious voodoo witchcraft tom-foolery going on here
    """
    category_id = request.GET.get("category_id", None)

    if question_id is None:
        question = None
    else:
        question = get_object_or_404(Question, pk=question_id)
        question.created_on=timezone.now()
        tags = question.tags.all()

    if request.POST:
        form = QuestionForm(request.POST, instance=question, created_by=request.user)
        if form.is_valid():
            form.save()
            if category_id:
                if question_id:
                    messages.success(request, "Question was successfully edited.")
                    return redirect(reverse("categories-detail", args=[category_id]))
                else:
                    messages.success(request, "Question was successfully appended.")
                    return redirect(reverse("categories-detail", args=[category_id]))
            else:
                if question_id:
                    messages.success(request, "Question was successfully edited.")
                    return redirect(reverse("questions-list"))
                else:
                    messages.success(request, "Question was successfully edited.")
                    return redirect(reverse("questions-list"))
    else:
        form = QuestionForm(instance=question, category_id=category_id)

    return render(request, "questions/edit.html", {
        "question": question,
        "form": form,
        "category_id": category_id,
    })


def delete(request, question_id):
    """
    Deletes a single question from the list
    TODO: Batch delete implemented in listview?
    """
    question = get_object_or_404(Question, pk=question_id)
    category_id = request.GET.get("category_id", None)

    if request.method == "POST":
        if question:
            question.delete()
        if category_id:
            context = messages.success(request, "Question was successfully deleted.")
            return redirect(reverse("categories-detail", args=[category_id,]))
        else:
            context = messages.success(request, "Question was successfully deleted.")
            return redirect(reverse("questions-list"), messages=[context,])

    return render(request, 'questions/delete.html', {
        "question": question,
        "category_id": category_id,
    })
