from django.contrib import admin

from .models import User, Listings, Category

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone", "email")

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Listings)