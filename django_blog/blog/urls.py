from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("posts/", views.posts, name="posts"),
]