from django.contrib import admin

from .models import User, Post, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)