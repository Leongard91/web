from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing_view, name="listing_view"),
    path("listings/create", views.create_new, name="create_listing"),
    path("watchlist", views.watchlist, name='watchlist'),
    path("categories", views.categories, name="categories"),
    path("winn", views.winn, name="winn")
]
