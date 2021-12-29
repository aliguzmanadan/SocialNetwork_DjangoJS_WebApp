
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("user/<str:username>", views.user_page, name="user_page"),
    path("follow_unfollow/<str:username>", views.follow_unfollow, name="follow_unfollow"),
    path("newpost", views.newpost, name="newpost"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API routes
    path("posts", views.new_post, name="new_post"),
    path("posts/<str:set_name>", views.get_posts, name="get_posts"),
    path("post/<int:post_id>", views.individual_post, name="individual_posts")
]
