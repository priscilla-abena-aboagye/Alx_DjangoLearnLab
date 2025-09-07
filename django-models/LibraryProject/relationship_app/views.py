from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.generic import DetailView

# Create your views here.

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

class LibraryView(DetailView):
    model = Library
    template_name = 'relationship_app/library_details.html'
    context_object_name = 'library'
    