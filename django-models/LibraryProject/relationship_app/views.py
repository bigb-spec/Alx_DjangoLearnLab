from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book
from .models import Library

# function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    # render into HTML template
    return render(request, "relationship_app/list_books.html", {"books": books})

# class-based view: detail of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"