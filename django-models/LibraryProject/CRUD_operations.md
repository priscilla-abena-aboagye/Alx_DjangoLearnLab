## Create book

```python
from bookshelf.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
print(book)
```

### output
1984

## Retrieve Book Instance

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")

# Display all attributes of the book
print(book.id, book.title, book.author, book.publication_year)
```

### output 
3 1984 George Orwell 1949

## Update book 
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

## Delete book
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