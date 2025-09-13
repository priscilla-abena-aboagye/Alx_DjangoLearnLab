import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from .models import *

# Query all books by a specific author.
author_name = "Peggy Oppong"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
for book in books_by_author:
    print(book.title)


# List all books in a library.
library_name = "Accra Central Library"
library = Library.objects.get(name=library_name)
for book in library.books.all():
    print(book)

# Retrieve the librarian for a library.
librarian = Librarian.objects.get(library=library)
print(librarian.name)