from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    followers = models.ManyToManyField("self", blank=True, null=True, symmetrical=False, related_name='+')
    follow_to = models.ManyToManyField('self', blank=True, null=True, symmetrical=False, related_name='+')
    def __str__(self):
        return f"Id:{self.pk}; {self.username}; followers: {self.followers.all().count()}; follow_to: {self.follow_to.all().count()}; posts: {self.posted_posts.all().count()}"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_posts") # need to bee filled (check)
    text = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, null=True, related_name='liked_posts')
    def __str__(self):
        return f"Id: {self.pk}; author: {self.author.username}; {str(self.timestamp)[:19]}; likes: {self.likes.all().count()}; comments: {self.comments.all().count()}; {self.text.split()[0]}"

class Comment(models.Model):
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_comments") # need to bee filled (check)
    text = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, null=True, related_name='liked_comments')
    def __str__(self):
        return f"Id: {self.pk}; author: {self.author.username}; {str(self.timestamp)[:19]}; likes: {self.likes.all().count()}; on post: id{self.on_post.pk}; {self.text.split()[0]}"
