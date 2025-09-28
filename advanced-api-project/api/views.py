from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class BookListCreateAPI(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Only users that are authenticated can create, but anyone can list
    def get_permissions(self):
        if self.request.method == "POST":  # Fix typo: must be uppercase POST
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    # Filtering by query parameters
    def get_queryset(self):
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author__id=author_id)
        return queryset
    
class BookDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Only authenticated users can update/delete, anyone can retrieve
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"

class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"

class BookCreateView(CreateView):
    model = Book
    fields = ["title", "publication_year", "author"]
    template_name = "book_form.html"

class BookUpdateView(UpdateView):
    model = Book
    fields = ["title", "publication_year", "author"]
    template_name = "book_form.html"

class BookDeleteView(DeleteView):
    model = Book
    template_name = "book_confirm_delete.html"
    success_url = "/books/"