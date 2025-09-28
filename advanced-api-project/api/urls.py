from django.urls import path
from .views import BookDetailAPI, BookListCreateAPI, BookCreateView, BookUpdateView, BookDeleteView, BookListView, BookDetailView

urlpatterns = [
    path("api/books/", BookListCreateAPI.as_view(), name="book-list-api"),
    path("api/books/<int:pk>/", BookDetailAPI.as_view(), name="book-detail-api"),

    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    path("books/update/<int:pk>/", BookUpdateView.as_view(), name="book-update"),
    path("books/delete/<int:pk>/", BookDeleteView.as_view(), name="book-delete"),

]