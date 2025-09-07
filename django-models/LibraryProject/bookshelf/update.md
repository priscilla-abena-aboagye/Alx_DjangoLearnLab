
```python
from bookshelf.models import Book

# Retrieve the book we created
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

print(book)
```

### output
Nineteen Eighty-Four