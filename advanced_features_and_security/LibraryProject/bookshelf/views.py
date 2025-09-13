from django.shortcuts import render

# Create your views here.
# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

# View books
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

# Create book
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        Book.objects.create(title=title, author=author)
        return redirect('book_list')
    return render(request, 'books/book_form.html')

# Edit book
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.save()
        return redirect('book_list')
    return render(request, 'books/book_form.html', {'book': book})

# Delete book
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')

# advanced_features_and_security/LibraryProject/LibraryProject/settings.py
# Application definition
# views.py
from django.shortcuts import render
from .models import Book
from .forms import BookSearchForm
from .forms import ExampleForm

def book_search(request):
    form = BookSearchForm(request.GET or None)
    books = []
    if form.is_valid():
        query = form.cleaned_data["query"]
        books = Book.objects.filter(title__icontains=query)  # Safe ORM filtering
    return render(request, "bookshelf/book_list.html", {"books": books, "form": form})