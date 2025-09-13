import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return []


# 2. List all books in a library
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return []


# 3. Retrieve the librarian for a library
def librarian_of_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


# Example usage
if __name__ == "__main__":
    print("Books by Author John Doe:", books_by_author("John Doe"))
    print("Books in Library Central Library:", books_in_library("Central Library"))
    print("Librarian of Central Library:", librarian_of_library("Central Library"))