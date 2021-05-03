from django.contrib import admin

<<<<<<< HEAD
from .models import User, Listings, Category
=======
from .models import User, Listings, Category, Comments, Bids
>>>>>>> 033d65887f968d7b50687a8ec462b81c16c05a9a

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone", "email")

admin.site.register(User, UserAdmin)
admin.site.register(Category)
<<<<<<< HEAD
admin.site.register(Listings)
=======
admin.site.register(Listings)
admin.site.register(Comments)
admin.site.register(Bids)
>>>>>>> 033d65887f968d7b50687a8ec462b81c16c05a9a
