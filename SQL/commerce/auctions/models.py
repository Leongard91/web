from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Username: {self.username}\nPhone: {self.phone}\nE-mail: {self.email}"

class Listings(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.FloatField(null=True)
    image = models.FileField(upload_to='auctions/uploads', default='auctions/uploads/No_img.jpg')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    
    categories = [()]#!!!!!!!!!!!!!!!!!!
    category = models#!!!!!!!!!!!!!!!!!!!!

    def __str__(self):
        return f"Listing: {title}\nPrice: ${price}\nAuthor: {author}"

