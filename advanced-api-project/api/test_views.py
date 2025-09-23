
"""
Unit tests for the Book API endpoints.

Covers:
- List (GET /api/books/)
- Create (POST /api/books/create/) - authenticated required
- Retrieve (GET /api/books/<pk>/)
- Update (PUT /api/books/update/<pk>/) - authenticated required
- Delete (DELETE /api/books/delete/<pk>/) - authenticated required
- Filtering, Searching, Ordering
- Permission enforcement (IsAuthenticated for write operations)

"""

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Author, Book


# Base endpoint paths
BASE_LIST = "/api/books/"              # GET list
BASE_CREATE = "/api/books/create/"     # POST create
BASE_UPDATE = "/api/books/update/{pk}/"   # PUT/PATCH update
BASE_DELETE = "/api/books/delete/{pk}/"   # DELETE delete
BASE_DETAIL = "/api/books/{pk}/"          # GET detail


class BookAPITestCase(APITestCase):
    def setUp(self):
        """
        Create test data: one user (for auth), one author, and several books.
        Also create a token for the user to use in authenticated requests.
        """
        # Create user for authenticated actions
        self.user = User.objects.create_user(username="tester", password="pass12345")
        self.token = Token.objects.create(user=self.user)

        # API client instances
        self.anon_client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Create an author
        self.author = Author.objects.create(name="George Orwell")

        # Create books with varying titles and years for filtering/search/order tests
        self.book1 = Book.objects.create(title="1984", publication_year=1949, author=self.author)
        self.book2 = Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author)
        self.book3 = Book.objects.create(title="A Modern Tale", publication_year=2020, author=self.author)

    # Basic CRUD tests
  
    def test_list_books(self):
        """GET /api/books/ should return all books and status 200."""
        resp = self.anon_client.get(BASE_LIST)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Expect at least the 3 created items
        self.assertIsInstance(resp.data, list)
        titles = {b["title"] for b in resp.data}
        self.assertTrue({"1984", "Animal Farm", "A Modern Tale"}.issubset(titles))

    def test_retrieve_book(self):
        """GET /api/books/<pk>/ returns the book detail."""
        resp = self.anon_client.get(BASE_DETAIL.format(pk=self.book1.pk))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("title"), "1984")
        self.assertEqual(resp.data.get("publication_year"), 1949)

    def test_create_book_unauthenticated_forbidden(self):
        """POST to create endpoint without auth should be 401 Unauthorized."""
        payload = {"title": "New Book", "publication_year": 2021, "author": self.author.pk}
        resp = self.anon_client.post(BASE_CREATE, data=payload, format="json")
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """POST to create endpoint with token should create and return 201."""
        payload = {"title": "New Book", "publication_year": 2021, "author": self.author.pk}
        resp = self.auth_client.post(BASE_CREATE, data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Ensure the book exists in DB
        exists = Book.objects.filter(title="New Book", publication_year=2021, author=self.author).exists()
        self.assertTrue(exists)

    def test_update_book_permissions(self):
        """PUT /api/books/update/<pk>/ requires auth; unauthenticated should be forbidden."""
        update_payload = {"title": "1984 - Updated", "publication_year": 1949, "author": self.author.pk}
        # Unauthenticated
        resp_anon = self.anon_client.put(BASE_UPDATE.format(pk=self.book1.pk), data=update_payload, format="json")
        self.assertIn(resp_anon.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        # Authenticated
        resp_auth = self.auth_client.put(BASE_UPDATE.format(pk=self.book1.pk), data=update_payload, format="json")
        # Accept 200 or 202 depending on implementation
        self.assertIn(resp_auth.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED, status.HTTP_204_NO_CONTENT))
        # Confirm update persisted
        self.book1.refresh_from_db()
        self.assertIn("Updated", self.book1.title)

    def test_delete_book_permissions(self):
        """DELETE /api/books/delete/<pk>/ requires auth and removes object."""
        # Unauthenticated delete attempt
        resp_anon = self.anon_client.delete(BASE_DELETE.format(pk=self.book2.pk))
        self.assertIn(resp_anon.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        # Authenticated delete
        resp_auth = self.auth_client.delete(BASE_DELETE.format(pk=self.book2.pk))
        # Accept 204 No Content or 200 OK depending on implementation
        self.assertIn(resp_auth.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        # Confirm deletion
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    # Filtering, Searching, Ordering

    def test_filter_by_publication_year(self):
        """Test filtering /api/books/?publication_year=<year>"""
        resp = self.anon_client.get(BASE_LIST, {"publication_year": 1949})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Should return only 1984 for year 1949
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["title"], "1984")

    def test_search_by_title(self):
        """Test search via ?search=... (title or author__name depending on config)."""
        resp = self.anon_client.get(BASE_LIST, {"search": "Animal"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.data]
        self.assertIn("Animal Farm", titles)

    def test_ordering_by_publication_year(self):
        """Test ordering via ?ordering=publication_year and descending with -publication_year."""
        # Ascending
        resp_asc = self.anon_client.get(BASE_LIST, {"ordering": "publication_year"})
        self.assertEqual(resp_asc.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp_asc.data]
        self.assertEqual(years, sorted(years))
        # Descending
        resp_desc = self.anon_client.get(BASE_LIST, {"ordering": "-publication_year"})
        self.assertEqual(resp_desc.status_code, status.HTTP_200_OK)
        years_desc = [b["publication_year"] for b in resp_desc.data]
        self.assertEqual(years_desc, sorted(years_desc, reverse=True))

    # Validation edge-cases

    def test_create_book_future_publication_year_fails(self):
        """If serializer validates publication_year (no future years), ensure it rejects future year."""
        import datetime
        next_year = datetime.date.today().year + 1
        payload = {"title": "Future Book", "publication_year": next_year, "author": self.author.pk}
        resp = self.auth_client.post(BASE_CREATE, data=payload, format="json")
        # Expect 400 Bad Request due to validation
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # Ensure not created
        self.assertFalse(Book.objects.filter(title="Future Book").exists())
