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
from rest_framework import generics, permissions, filters 
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework 

# Book CRUD Views

class BookListView(generics.ListAPIView):
    """
    GET /api/books/?title=xyz&author=1&publication_year=2020
    GET /api/books/?search=Harry
    GET /api/books/?ordering=title
    GET /api/books/?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # ✅ Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']  # Filtering
    search_fields = ['title', 'author__name']  # Searching
    ordering_fields = ['title', 'publication_year']  # Ordering
    ordering = ['title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single book by ID.
    Read-only, no authentication required.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Remove a book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
