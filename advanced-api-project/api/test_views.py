from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create user for authentication tests
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Create an author and a book
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )

        # Define URLs
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', args=[self.book.id])
        self.book_create_url = reverse('book-create')
        self.book_update_url = reverse('book-update', args=[self.book.id])
        self.book_delete_url = reverse('book-delete', args=[self.book.id])

    def test_list_books_without_auth(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_requires_login(self):
        data = {
            "title": "New Book",
            "publication_year": 2021,
            "author": self.author.id
        }
        # Try creating without login
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Now login and retry
        login_successful = self.client.login(username="testuser", password="password123")  # ✅ using self.client.login
        self.assertTrue(login_successful)

        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")

    def test_update_book_requires_login(self):
        data = {
            "title": "Updated Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        # Without login
        response = self.client.put(self.book_update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # With login
        self.client.login(username="testuser", password="password123")  # ✅
        response = self.client.put(self.book_update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")

    def test_delete_book_requires_login(self):
        # Without login
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # With login
        self.client.login(username="testuser", password="password123")  # ✅
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
