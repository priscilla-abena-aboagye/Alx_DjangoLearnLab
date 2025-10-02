## Django Blog Authentication System Documentation

This explains how the system works, how users interact with it, and how developers can test and extend the functionality.

### 1. Overview
The authentication system enables users to:

- Register for a new account

- Register for a new account

- Login to access personalized features

- Manage their profile (update personal information like email, bio, profile picture, etc.)

It is built using Django’s built-in authentication framework, with some custom extensions for registration and profile management.

### 2.Components
- Registration
- login
- Profile management
- Blog features

## Blog Features
- Post
- Create post
- Delete post
- Update post

### 3.URL structure
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("posts/", views.posts, name="posts"),

    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]
```

### 4. Templates
- base.html
- login.html
- posts.html
- profile.html
- register.html
- post_confirm_delete.html
- post_detail.html
- post form.html
- post_list.html

### 5.Security
- CSRF Protection: All forms include CSRF tokens.

- Password Hashing: Django securely hashes passwords using PBKDF2 by default.

- Login Required: The profile page is protected with ```@login_required.```

- Session Management: Secure session cookies prevent unauthorized access.


