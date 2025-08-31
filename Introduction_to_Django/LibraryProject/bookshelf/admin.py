from django.contrib import admin
from .models import Book

admin.site.register(Book)

# Register your models here.

class BookAdmin():
    list_display = ("title", "author", "publication_year")
    list_filter = ("publication_year", "author")
    search_feild = ("title", "author")
