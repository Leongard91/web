from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Post, Comment

class NewPostForm(forms.Form):
    post = forms.CharField(label="New Post", max_length=255, widget=forms.Textarea(attrs={'class': 'post_form'}))


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    if request.method == "POST":
        if request.user.is_authenticated and request.POST['post']:
            text = request.POST['post']
            try: Post.objects.create(author=request.user, text=text)
            except: HttpResponse('Insert Error')
            return HttpResponseRedirect(reverse('index'))
        return render(request, "network/index.html", {
            'message': "Could not post empty.",
            'post_form': NewPostForm(),
            'posts': posts
        })
    # How to implemment likes?!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return render(request, "network/index.html", {
        'post_form': NewPostForm(),
        'posts': posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")