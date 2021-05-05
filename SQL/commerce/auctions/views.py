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
    cat_choices= [(0, 'Categories')] + [(category.pk, category.category_name) for category in Category.objects.all()]
    title = forms.CharField(label="Title", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Listing Title', 'style': "width:100%; margin-bottom: 20px;"}))
    category = forms.ChoiceField(label="Choose Category", required=False, widget=forms.Select(attrs={'style': "width:100%; margin-bottom: 20px;"}), choices=cat_choices)
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"rows":5, "cols":4, 'style': "width:100%;"}))
    price = forms.DecimalField(label="Price", decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': '$ 0.00', 'style': "width:100%; margin-bottom: 20px;"}))
    image = forms.URLField(label="Enter IMAGE's URL", required=False, widget=forms.URLInput(attrs={'placeholder': 'URL', 'style': "width:100%; margin-bottom: 20px;"}))

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
    form = Listings.objects.get(pk=int(listing_id))
    current_user = User.objects.get(pk=request.session['user_id'])
    
    # get all listings categories
    try: cat_list = ', '.join([category.category_name for category in form.category.all()])
    except: cat_list = ''
    price = "${:,.2f}".format(form.price)

    # get max bid
    try: max_bid = max([bit_object.bid for bit_object in form.bids_on_listing.all()]) #!!!!
    except ValueError: max_bid = 0
    max_bid_html = "${:,.2f}".format(max_bid)

    # check is listing in userr watchlist
    in_watchlist = False
    in_users_watchlists = [user.pk for user in form.in_users_watchlists.all()]
    if request.session['user_id'] in in_users_watchlists: in_watchlist = True
    
    if request.method == 'POST':
        
        # adding(removing) to watchlist
        watchlist_command = request.POST['watchlist'] # TRY GET or chenge or replase bid post aper!!!!!!
        if watchlist_command !='' and watchlist_command == "add":
            form.in_users_watchlists.add(current_user)
            return HttpResponseRedirect(f"/listings/{form.pk}")
        elif watchlist_command !='' and watchlist_command == "remove":
            form.in_users_watchlists.remove(current_user)
            return HttpResponseRedirect(f"/listings/{form.pk}")

        # adding bid
        #proposed_bid = request.POST['bid']
        #if proposed_bid == '': proposed_bid = 0
        #if proposed_bid < form.price or proposed_bid < max_bid:
        #    return render(request, "auctions/listing.html", {
        #        'message': "Bed should be greater then max bid or equal the Price (if no bids).",
        #        'in_watchlist': in_watchlist,
        #        'in_watchlists':in_users_watchlists,
        #        "form": form,
        #        'price': price,
        #        'max_bid': max_bid,
        #        'max_bid_html': max_bid_html,
        #        'cat_list': cat_list
        #    })
        
        
    return render(request, "auctions/listing.html", {
        'in_watchlist': in_watchlist,
        'in_watchlists':in_users_watchlists,
        "form": form,
        'price': price,
        'max_bid': max_bid,
        'max_bid_html': max_bid_html,
        'cat_list': cat_list
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
            if not 'http' in image: image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/330px-No-Image-Placeholder.svg.png'
            try: category = Category.objects.get(pk=form.cleaned_data['category'])
            except: category = 0
            initial = {'title':title, 'description':description, 'price':price, 'author':author, 'image':image}
            try:
                new_listing = Listings(title=title, description=description, price=price, author=author, image=image)
                new_listing.save()
                if category != 0:
                    new_listing.category.add(category)
            except IntegrityError: 
                return render(request, "auctions/new_listing.html", {
                "message": "Insert Error.",
                'form': NewListingform(initial=initial)
                })
            link = f"/listings/{new_listing.pk}"
            return HttpResponseRedirect(link)
        return render(request, "auctions/new_listing.html", {
            "message": "Form Error",
            'form': NewListingform(initial=initial) })

    return render(request, "auctions/new_listing.html", {
        "form" : NewListingform()
    })
