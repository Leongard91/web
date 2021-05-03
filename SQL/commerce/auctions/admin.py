from django.contrib import admin

from .models import User, Listings, Category, Comments, Bids

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone", "email")

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Listings)
admin.site.register(Comments)
admin.site.register(Bids)
