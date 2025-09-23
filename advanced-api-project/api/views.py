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


