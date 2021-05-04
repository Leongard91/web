from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django import forms
from django.db.models import Count

from .models import User, Category, Listings, Bids, Comments


class NewListingform(forms.Form):
    cat_choices= [('', 'Categories')] + [(category.pk, category.category_name) for category in Category.objects.all()]
    title = forms.CharField(label="Title", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Listing Title', 'style': "width:100%; margin-bottom: 20px;"}))
    category = forms.ChoiceField(label="Choose Category", widget=forms.Select(attrs={'style': "width:100%; margin-bottom: 20px;"}), choices=cat_choices)
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"rows":5, "cols":4, 'style': "width:100%;"}))
    price = forms.DecimalField(label="Price", decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': '$ 0.00', 'style': "width:100%; margin-bottom: 20px;"}))
    image = forms.URLField(label="Enter IMAGE's URL", widget=forms.URLInput(attrs={'placeholder': 'URL', 'style': "width:100%; margin-bottom: 20px;"}))

    # if file upload model
    #image = forms.FileField(label="Upload Photo", widget=forms.FileInput(attrs={'style': "width:100%; margin-bottom: 20px;"}))


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
            request.session['user_id'] = User.objects.get(username=username).pk
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
        request.session['user_id'] = User.objects.get(username=username).pk
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing_view(request, listing_id):
    if request.method == 'POST':
        pass
    form = Listings.objects.get(pk=listing_id)
    bids_numb = len(form.bids_on_listing.filter(listing=form))
    return render(request, "auctions/listing.html", {
        "form": form,
        'bids_numb': bids_numb
    })


def create_new(request):
    if request.method == "POST":
        form = NewListingform(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            author = User.objects.get(pk=request.session['user_id'])
            image = form.cleaned_data['image']  # if file upload model : image = request.FILES['image']
            category = Category.objects.get(pk=form.cleaned_data['category'])
            try:
                new_listing = Listings(title=title, description=description, price=price, author=author, image=image)
                new_listing.save()
                new_listing.category.add(category)
            except IntegrityError: 
                return render(request, "auctions/new_listing.html", {
                "message": "Insert Error."
                })
            return HttpResponseRedirect(f"listings/{new_listing.pk}")
        return render(request, "auctions/new_listing.html", {
            "message": form.errors })

    return render(request, "auctions/new_listing.html", {
        "form" : NewListingform()
    })
