"""
Views for Book API
------------------
- BookListCreateView:
    Handles GET (list all books) and POST (create book).
    Read allowed for everyone, write restricted to authenticated users.

- BookDetailView:
    Handles GET (single book), PUT/PATCH (update), DELETE (remove).
    Read allowed for everyone, write restricted to authenticated users.

Customizations:
- Permissions enforced per HTTP method.
- Filtering support (year, author).
"""

from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# Generic Views for Book

# List all books / Create new book
class BookListCreateView(generics.ListCreateAPIView):
    """
    GET: Return a list of all books.
    POST: Create a new book (authenticated users only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Allow read-only for unauthenticated, but restrict create to logged in users
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


# Retrieve / Update / Delete a single book
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a book by ID.
    PUT/PATCH: Update a book (authenticated users only).
    DELETE: Remove a book (authenticated users only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Allow read-only for unauthenticated, restrict update/delete to logged in users
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

def get_queryset(self):
    queryset = Book.objects.all()
    year = self.request.query_params.get("year")
    author = self.request.query_params.get("author")
    if year:
        queryset = queryset.filter(publication_year=year)
    if author:
        queryset = queryset.filter(author__name__icontains=author)
    return queryset

