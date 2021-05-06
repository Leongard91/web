from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from django.core.exceptions import ValidationError
from datetime import datetime

class User(AbstractUser):
    phone = models.CharField(max_length=20)
    def __str__(self):
        return f"Username: {self.username}\nPhone: {self.phone}\nE-mail: {self.email}"


class Category(models.Model):
    category_name = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return f"{self.category_name}"


class Listings(models.Model):
    # if file upload model:
    #def user_directory_path(instance, filename):
    #    return '{0}/media/auctions/user_{1}/{2}'.format(os.getcwd(), instance.author.id, filename)
    #def validate_file_extension(value):
    #   ext = os.path.splitext(value.name)[1]
    #    valid_extensions = ['.png','.jpg']
    #    if not ext in valid_extensions:
    #        raise ValidationError(u'Need png or jpg image to be uploaded')
    # if file upload model : image = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension], blank=True, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(null=True, max_digits=7, decimal_places=2)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_from_user") 
    image = models.URLField() 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='listings_on_category')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    in_users_watchlists = models.ManyToManyField(User, blank=True, related_name="listings_in_watchlist")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='won_actions', blank=True, null=True)
    status= models.CharField(max_length=10, choices=(('a','active'), ('s','sold'), ('d','deleted')), null=True, blank=True)
    def __str__(self):
        return f"id: {self.pk}/ Listing: {self.title}/ Status: {self.status}/ Category: '{self.category}'/ Price: ${self.price}/ Author: {self.author.username}/ Creation date: {self.date}"


class Bids(models.Model):
    bid = models.FloatField()
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="bids_from_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, related_name='bids_on_listing')
    def __str__(self):
        return f"id: {self.pk}; bid: {self.bid}; date: {self.date}; from user: {self.from_user.username}; on listing: {self.listing.title}"


class Comments(models.Model):
    comment = models.TextField(max_length=500)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="comments_from_user")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, related_name='comments_on_listing')
    def __str__(self):
        return f"id: {self.pk}; from: {self.from_user.username}; on listing: {self.listing.title}"


