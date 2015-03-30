import os
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib import messages

def home(request):
    """
    Default home view
    """
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created!")
            return HttpResponseRedirect(request.get_full_path())
    else:
        form = UserForm()

    return render(request, 'home.html', {
        "form": form,
    })
