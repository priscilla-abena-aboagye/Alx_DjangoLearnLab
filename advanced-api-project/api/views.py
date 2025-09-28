from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters import rest_framework as drf_filters

class BookListCreateAPI(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Only users that are authenticated can create, but anyone can list
    def get_permissions(self):
        if self.request.method == "POST":  
            return [IsAuthenticated()]
        return [AllowAny()]
    
    # Filtering , searching and ordering
    filter_backends = [
        drf_filters.DjangoFilterBackend,  # filtering
        filters.SearchFilter,             # searching
        filters.OrderingFilter            # ordering
    ]

    filterset_fields = ['title', 'author', 'publication_year']  
    search_fields = ['title', 'author__name']                  
    ordering_fields = ['title', 'publication_year']             
    ordering = ['title']    
    
class BookDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    


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