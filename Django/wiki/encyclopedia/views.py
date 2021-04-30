from django.shortcuts import render

from django import forms
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from random import choice
from . import util


class NewEntryForm(forms.Form):
    name = forms.CharField(label="Page Name", widget=forms.TextInput(attrs={'placeholder': 'Page Name', 'style': "width:100%; margin-bottom: 20px;"}))
    content = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={"rows":5, "cols":20, 'style': "width:100%;"}))
 
class EditForm(forms.Form):
    content = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={"rows":5, "cols":20, 'style': "width:100%;"}))


def search(f):
    def wrapper(request, *args, **kwargs):
        if request.method == "POST":
            try:
                search_val = request.POST['q']
            except: return f(request, *args, **kwargs)
            if search_val in util.list_entries():
                return HttpResponseRedirect(f'/wiki/{search_val}')
            return HttpResponseRedirect(f'/search/{search_val}')
        return f(request, *args, **kwargs)
    return wrapper

@search
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

@search
def get(request, name):
    if name in util.list_entries():
        content = util.get_entry(name)
        ready_content= util.turn_to_HTML(content)
        return render(request, "encyclopedia/get.html", {
            "name": name,
            "content" : ready_content
        })
    else: return render(request, "encyclopedia/error.html")

@search
def s_res(request, name):
    matches = []
    for entry_name in util.list_entries():
        if name in entry_name:
            matches.append(entry_name)
    return render(request, "encyclopedia/search_result.html", {
        'matches': matches
    })

@search
def create_new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            name_val = form.cleaned_data["name"]
            if name_val in util.list_entries():
                return render(request, "encyclopedia/create_new.html", {
                    "message" : 'Page already exists!',
                    "form": form
                })
            content_val = form.cleaned_data["content"]
            util.save_entry(name_val, content_val)
            return HttpResponseRedirect(f'/wiki/{name_val}')
        return render(request, "encyclopedia/create_new.html", {
                    "message" : 'Not valid input!',
                    "form": form
                })
    return render(request, "encyclopedia/create_new.html", {
        "form": NewEntryForm()
    })

@search
def edit(request, name):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content_val = form.cleaned_data["content"]
            util.save_entry(name, content_val)
            return HttpResponseRedirect(f'/wiki/{name}')
    content = util.get_entry(name)
    initial = { 'content' : content }
    form = EditForm(initial=initial)
    return render(request, "encyclopedia/edit.html", {
        "name": name,
        "form": form
    })

def random(request):
    names = util.list_entries()
    name = choice(names)
    return HttpResponseRedirect(f"/wiki/{name}")