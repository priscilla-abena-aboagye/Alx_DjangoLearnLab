### Retrieve Book Instance

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")

# Display all attributes of the book
print(book.id, book.title, book.author, book.publication_year)
```

### output 
3 1984 George Orwell 1949