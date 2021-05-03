from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django import forms

from .models import User, Category, Listings


class NewListingform(forms.Form):
    title = forms.CharField(label="Title", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Listing Title', 'style': "width:100%; margin-bottom: 20px;"}))
    category = forms.CharField(label="Choose Category", max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Categories', 'style': "width:100%; margin-bottom: 20px;"}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"rows":5, "cols":4, 'style': "width:100%;"}))
    price = forms.DecimalField(label="Price", decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': '$ 0.00', 'style': "width:100%; margin-bottom: 20px;"}))
    image = forms.FileField(label="Upload Photo")


def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, phone=phone)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing_view(request, listing_id):
    return HttpResponse("Not done yyet!!")


def create_new(request):
    if request.method == "POST":
        pass
    return render(request, "auctions/new_listing.html", {
        "form" : NewListingform()
    })
