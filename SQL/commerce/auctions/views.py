from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django import forms
from django.db.models import Count
from django.contrib.auth.decorators import login_required

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
    instance ={}
    forms = Listings.objects.filter(status='a')
    if forms != None:
        instance['forms'] = forms
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! price format
    return render(request, "auctions/index.html", instance)


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
    
    # get all listings categories
    try: cat_list = ', '.join([category.category_name for category in form.category.all()])
    except: cat_list = ''
    price = "${:,.2f}".format(form.price)

    # get max bid
    try: max_bid = max([bit_object.bid for bit_object in form.bids_on_listing.all()])
    except ValueError: max_bid = 0
    if max_bid != 0: max_bid_author = form.bids_on_listing.get(bid=max_bid).from_user
    else: max_bid_author = form.author
    max_bid_html = "${:,.2f}".format(max_bid)

    # check is listing in userr watchlist
    in_watchlist = False
    in_users_watchlists = [user.pk for user in form.in_users_watchlists.all()]
    try: 
        if request.session['user_id'] in in_users_watchlists: in_watchlist = True
    except KeyError: pass

    instance = {
        'in_watchlist': in_watchlist,
        'in_watchlists':in_users_watchlists,
        "form": form,
        'price': price,
        'max_bid': max_bid,
        'max_bid_html': max_bid_html,
        'cat_list': cat_list
    }

    # get comments uder listing
    comments = form.comments_on_listing.all().order_by('-date', '-pk')
    if len(comments) > 0: instance['comments'] = comments

    # check is user winner
    try:
        if max_bid_author.pk == request.session['user_id'] and form.status == "s": 
            instance['info'] = "Your Bid Winn! Please contact to author."
    except KeyError: pass

    if request.method == 'POST':
        current_user = User.objects.get(pk=request.session['user_id'])

        # listings closing
        if request.POST.get('close', False):
            if max_bid == 0: max_bid_html = price
            form.winner = max_bid_author
            form.status = 's'
            form.save()
            instance['info'] = f"Sold to {max_bid_author.username} by {max_bid_html}! Please contact to winner."
            return render(request, "auctions/listing.html", instance)
        if request.POST.get('delete', False):
            form.delete()
            instance = {}
            instance['info'] = "Deleted"
            return render(request, "auctions/index.html", instance)

        # adding bid
        if request.POST.get('bid', False):
            try: proposed_bid = float(request.POST.get('bid', False))
            except TypeError: 
                instance['message'] = "Enter a number in a bid."
                return render(request, "auctions/listing.html", instance)
            if proposed_bid < form.price or proposed_bid < max_bid or proposed_bid == max_bid :
                instance['message'] = "Bid should be greater then max bid or equal the Price (if no bids)."
                return render(request, "auctions/listing.html", instance)
            try:
                new_bid = Bids(bid=proposed_bid, from_user=current_user, listing=form)
                new_bid.save()
            except IntegrityError:
                instance['message'] = "Invalid bid."
                return render(request, "auctions/listing.html", instance)
            proposed_bid_html = "${:,.2f}".format(proposed_bid)
            form.price = float(proposed_bid)
            form.save()
            instance['price'] = "${:,.2f}".format(proposed_bid)
            instance['info'] = f"Your Bid in {proposed_bid_html} accepted!"
            instance['max_bid'] = proposed_bid
            instance['max_bid_html'] = proposed_bid_html
            return render(request, "auctions/listing.html", instance)

        # adding comments
        if request.POST.get("add_comment", False):
            new_comment = request.POST.get("add_comment", False)
            new_comment_in = Comments(comment=new_comment, from_user=current_user, listing=form)
            new_comment_in.save()
            return HttpResponseRedirect(f"/listings/{form.pk}")

        # adding(removing) to watchlist
        if request.POST.get('watchlist', False):
            watchlist_command = request.POST.get('watchlist', False) # TRY GET or chenge or replase bid post aper!!!!!!
            if watchlist_command !='' and watchlist_command == "add":
                form.in_users_watchlists.add(current_user)
                return HttpResponseRedirect(f"/listings/{form.pk}")
            elif watchlist_command !='' and watchlist_command == "remove":
                form.in_users_watchlists.remove(current_user)
                return HttpResponseRedirect(f"/listings/{form.pk}")
    return render(request, "auctions/listing.html", instance)

@login_required(login_url='login')
def create_new(request):
    if request.method == "POST":
        form = NewListingform(request.POST) # + request.FILES
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
                new_listing = Listings(title=title, description=description, price=price, author=author, image=image, status='a')
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
            "message": "Form Error. Please check image URL.",
            'form': NewListingform()})

    return render(request, "auctions/new_listing.html", {
        "form" : NewListingform()
    })
