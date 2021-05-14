from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post, Comment

class NewPostForm(forms.Form):
    post = forms.CharField(label="New Post", max_length=255, widget=forms.Textarea(attrs={'class': 'post_form'}))


def index(request):
    posts = Post.objects.all().order_by('-timestamp')

    # Paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # add new post
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

    return render(request, "network/index.html", {
        'post_form': NewPostForm(),
        'posts': posts
    })

@login_required(login_url='login')
def following(request):
    current_user = User.objects.get(pk=request.user.pk)
    follow_to = current_user.follow_to.all()
    unsorted_d = {}
    for i in follow_to:
        for post in i.posted_posts.all():
            try: unsorted_d[post.timestamp] = post
            except: continue # If two posts with identical timestamp
    
    d = dict(sorted(unsorted_d.items(), reverse=True))
    posts = list(d.values())

    # Paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'network/following.html', {'posts': posts})


def user_view(request, id):
    instance = {}
    account = User.objects.get(pk=id)

    # add(delete) to followers
    if request.method == 'POST':
        if request.POST.get("follow_button", False) == 'follow':
            account.followers.add(request.user)
            request.user.follow_to.add(account)
        elif request.POST.get("follow_button", False) == 'unfollow':
            account.followers.remove(request.user)
            request.user.follow_to.remove(account)
        return HttpResponseRedirect(f'/user/{account.pk}')

    posted_posts = account.posted_posts.all().order_by('-timestamp')
    instance['posts_count'] = posted_posts.count()

    # Paginator
    paginator = Paginator(posted_posts, 10)
    page_number = request.GET.get('page')
    posted_posts = paginator.get_page(page_number)

    followers = account.followers.all().count()
    follow_to = account.follow_to.all().count()
    instance['account'] = account
    instance['followers'] = followers
    instance['follow_to'] = follow_to
    instance['posts'] = posted_posts
    

    # check is current user on his own page
    on_own_page = False
    if account.pk == request.user.pk: on_own_page = True
    instance['on_own_page'] = on_own_page

    # check is current user is followed
    is_followed = False
    if request.user.pk in [follower.pk for follower in account.followers.all()]:
        is_followed = True
    instance['is_followed'] = is_followed
    
    return render(request, "network/user.html", instance)


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
