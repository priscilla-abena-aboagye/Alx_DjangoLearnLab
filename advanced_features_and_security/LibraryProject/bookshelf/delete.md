```python
from bookshelf.models import Book

# Retrieve the book we updated
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

# Try retrieving all books again
books = Book.objects.all()
print(books)
```
### output
```
<QuerySet [<Book: Things fall apart>, <Book: Ego is the enemy>]>
```