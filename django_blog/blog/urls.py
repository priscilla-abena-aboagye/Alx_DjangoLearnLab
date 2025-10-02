from django.urls import path
from . import views
from .views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("profile/", views.profile_view, name="profile"),

    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),

    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment-create"),
    path("post/<int:pk>/comments/<int:comment_pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("post/<int:pk>/comments/<int:comment_pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),



]