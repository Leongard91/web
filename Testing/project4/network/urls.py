
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('user/<int:id>', views.user_view, name="user_page"),
    path('following', views.following, name='following'),
    path('post_reduction/<int:post_id>', views.post_reduction, name='reduction'),
    path('like', views.like, name="like"),
    path('comment', views.comment, name='comment')
]
