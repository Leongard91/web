from django.contrib.auth.models import AbstractUser
from django.db import models
import os


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return f"Username: {self.username}\nPhone: {self.phone}\nE-mail: {self.email}"


class Category(models.Model):
    category_name = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return f"{self.category_name}"


class Listings(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/media/auctions/user_{1}/{2}'.format(os.getcwd(), instance.author.id, filename)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.FloatField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings") 
    image = models.FileField(upload_to=user_directory_path, null=True)
    category = models.ManyToManyField(Category, blank=True, related_name='listings')
    def __str__(self):
        return f"Listing: {self.title}/ Category: '{self.category}'/ Price: ${self.price}/ Author: {self.author.username}"

