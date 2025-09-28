from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Only users that are authenticated can create, but anyone can list
    def get_permissions(self):
        if self.request.method == "Post":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    # filtering by query parameters
    def get_queryset(self):
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author__id=author_id)
        return queryset
    
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Only authenticated users can update/delete, anyone can retrieve
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

