from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library

# function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    # render into HTML template
    return render(request, "relationship_app/list_books.html", {"books": books})