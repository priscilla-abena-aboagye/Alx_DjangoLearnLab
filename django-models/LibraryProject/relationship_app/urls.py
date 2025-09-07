from django.urls import path 
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("books", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name='library_detail'),

    path("register", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    path('admin_view/', views.admin_view, name='admin_view'),
    path('librarian_view/', views.librarian_view, name='librarian_view'),
    path('member_view/', views.member_view, name='member_view'),

    path('books/', views.list_books, name='list_books'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('book/delete/<int:pk>/', views.delete_book, name='delete_book'),
]

