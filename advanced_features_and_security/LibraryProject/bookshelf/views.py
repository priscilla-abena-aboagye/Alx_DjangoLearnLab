from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import ExampleForm

# Create your views here.
# can view books
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/list_books.html", {"books": books})


# can add books
@permission_required('bookshelf.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

# can edit books
@permission_required('bookshelf.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = ExampleForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})

# can delete books
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'bookshelf/book_confirm.html', {'book': book})
    