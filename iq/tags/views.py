import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from .models import Tag


def list_(request):
    """
    Display a list of tags
    """
    tags = Tag.objects.all()
    return render(request, "tags/list.html", {
        "tags": tags,
    })

def detail(request, tag_id):
    """
    List attributes of a given tag
    specified by tag_id
    """
    t = get_object_or_404(Tag, pk=tag_id)
    return render(request, 'tags/detail.html', {
        "tag": t,
    })
