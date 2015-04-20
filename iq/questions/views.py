import datetime
#import elasticsearch
import json
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from iq.categories.models import Category
from iq.tags.models import Tag
from .forms import QuestionForm, QuestionSearchForm
from .models import Question, CategoryQuestion

#TODO: Integrate Elastic Models into this
#def esIndex(request, question_id):
#    """
#    Indexes a question document in Elasticsearch
#    """
#    if question_id is not None:
#        q = get_object_or_404(Question, pk=question_id)
#        if q.tags:
#            tags = [tag.name for tag in q.tags.all()]
#        else:
#            tags = None
#        es = elasticsearch.Elasticsearch() # localhost:9200
#        print("\n--------- Document info: -------------------------")
#        print("[ Object ] Body:       ", q.body)
#        print("[ Object ] Answer:     ", q.answer)
#        print("[ Object ] Difficulty: ", q.difficulty)
#        print("[ Object ] Created by: ", q.created_by.username)
#        print("[ Object ] Created on: ", q.created_on)
#        print("[ Object ] Tags:       ", tags)
#        print("--------- Progress: ------------------------------")
#        print("[ Status ] Indexing ...")
#        es.index(index='questions', doc_type='question', id=q.pk, body={
#            'body': q.body,
#            'answer': q.answer,
#            'difficulty': q.difficulty,
#            'tags': tags,
#            'created_on': q.created_on,
#            'created_by': q.created_by.username
#        })
#        print("[Complete] Document indexed.\n")
#    else:
#        print("[ Failed ] Invalid Question ID - Aborting\n")
#    return redirect(reverse("questions-list"))
#
#def esRetrieve(request, question_id):
#    """
#    Retrieves a question document from Elasticsearch
#    """
#    if question_id is not None:
#        es = elasticsearch.Elasticsearch() # localhost:9200
#        print("\n--------- Progress: ------------------------------")
#        print("[ Status ] Searching ...")
#        results = es.get(index='questions', doc_type='question', id=question_id)
#        if results:
#            print("[Complete] Document was found.")
#            print("[Complete] Returning JSON Document ...")
#            print("--------- Results: -------------------------------")
#            print("[ Object ] Body:       ", results["_source"]["body"])
#            print("[ Object ] Answer:     ", results["_source"]["answer"])
#            print("[ Object ] Difficulty: ", results["_source"]["difficulty"])
#            print("[ Object ] Created by: ", results["_source"]["created_by"])
#            print("[ Object ] Created on: ", results["_source"]["created_on"])
#            print("[ Object ] Tags:       ", results["_source"]["tags"])
#            print("\n")
#    else:
#        print("[ Failed ] Invalid Question ID - Aborting\n")
#    return redirect(reverse("questions-list"))

@login_required
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

@login_required
def create(request):
    """
    Create a new question
    """
    return _edit(request, question_id=None)

@login_required
def edit(request, question_id):
    """
    Edit an existing question
    """
    return _edit(request, question_id)

def _edit(request, question_id):
    """
    Edit a single question and it's attributes
    """
    category_id = request.GET.get("category_id", None)

    if question_id is None:
        question = None
        tags = None
    else:
        question = get_object_or_404(Question, pk=question_id)
        question.created_on=timezone.now()
        tags = question.tags.all()

    if request.POST:
        if request.user.is_authenticated() == True:
            form = QuestionForm(
                    request.POST,
                    instance=question,
                    created_by=request.user
            )

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
                    messages.success(request, "Question was successfully created.")
                    return redirect(reverse("questions-list"))
    else:
        form = QuestionForm(instance=question, category_id=category_id)

    tags = json.dumps([str(tag) for tag in Tag.objects.all()])

    return render(request, "questions/edit.html", {
        "form": form,
        "tags": tags,
        "question": question,
        "category_id": category_id,
    })

@login_required
def delete(request, question_id):
    """
    Deletes a single question from the list
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
