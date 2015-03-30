import datetime
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from iq.questions.models import Question, CategoryQuestion
from .forms import CategoryForm
from .models import Category


def list_(request):
    """
    Lists all categories, starting with the most
    recent category.
    """
    categories = Category.objects.order_by('-created_on')

    return render(request, "categories/list.html", {
        "categories": categories,
    })


def detail(request, category_id):
    """
    Lists all questions in all categories
    starting with the most recent category
    posted.
    """
    cat = get_object_or_404(Category, pk=category_id)
    questions = Question.objects.filter(categoryquestion__category=cat)

    return render(request, 'categories/detail.html', {
        "category": cat,
        "questions": questions,
    })


def printout(request, category_id):
    """
    References a raw HTML page suitable for printing
    out onto paper
    """
    cat = get_object_or_404(Category, pk=category_id)
    questions = Question.objects.filter(categoryquestion__category=cat)

    return render(request, 'categories/printout.html', {
        "category": cat,
        "questions": questions,
    })


def printout_applicant(request, category_id):
    """
    References a raw HTML page suitable for printing
    out onto paper
    """
    cat = get_object_or_404(Category, pk=category_id)
    questions = Question.objects.filter(categoryquestion__category=cat)

    return render(request, 'categories/printout_applicant.html', {
        "category": cat,
        "questions": questions,
    })


def create(request):
    """
    Create a single category
    """
    return _edit(request, category_id=None)


def edit(request, category_id):
    """
    Edit an existing category
    """
    return _edit(request, category_id)


def _edit(request, category_id):
    """
    Edit a single category and it's attributes
    """
    if category_id is None:
        category = None
    else:
        category = get_object_or_404(Category, pk=category_id)

    if request.POST:
        form = CategoryForm(request.POST, instance=category, created_by=request.user)
        if form.is_valid():
            form.save()
            if category_id:
                context = messages.success(request, '%s was successfully modified.' % category.name)
                return redirect(reverse("categories-list"), messages=[context,])
            else:
                context = messages.success(request, "Category was successfully created.")
                return redirect(reverse("categories-list"), messages=[context,])
    else:
        form = CategoryForm(instance=category)

    return render(request, "categories/edit.html", {
        "category": category,
        "form": form,
    })


def delete(request, category_id):
    """
    Deletes a single category from the list
    """
    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        if category:
            name = category.name
            category.delete()
            context = messages.success(request, "%s was successfully deleted." % name)
        return redirect(reverse("categories-list"), messages=[context,])

    return render(request, 'categories/delete.html', {
        "category": category,
    })
