from . import views
from django.urls import path 

urlpatterns = [
    path('books/', views.book_list, name='list_books'),  # list all books
    path('add_book/', views.add_book, name='add_book'),  # add a new book
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),  # edit a book
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'), 
]