import json
import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from .models import Tag

def to_json(request):
    tags = Tag.objects.all()

    objs = {"results": []}
    for tag in tags:
        objs['results'].append({"id": tag.name, "text": tag.name})

    return HttpResponse(json.dumps(objs), content_type="application/json")
