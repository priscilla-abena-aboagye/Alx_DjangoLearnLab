import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from .models import *

# Query all books by a specific author.
author = Author.objects.get(name="Peggy Oppong")
books_by_author = Book.objects.filter(author=author)
for book in books_by_author:
    print(book.title)


# List all books in a library.
library = Library.objects.get(name='End of the tunnel')
for book in library.books.all():
    print(book.name)

# Retrieve the librarian for a library.
librarian = Librarian.objects.get(library=library)
print(librarian.name)