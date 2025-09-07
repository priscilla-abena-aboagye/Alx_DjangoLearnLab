from django.urls import path
from . import views
from .views import LibraryView

urlpatterns = [
    path("books", views.list_books, name="list_books"),
    path("library/<int:pk>/", LibraryView.as_view(), name='library_detail'),
]

