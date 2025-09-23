from django.db import models

class Author(models.Model):
    """
    Author model stores information about book authors.
    One author can have many books.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model stores information about individual books.
    Each book is linked to a single Author (ForeignKey).
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
