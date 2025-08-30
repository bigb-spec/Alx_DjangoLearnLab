from django.contrib import admin
from bookshelf.models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns shown in list view
    list_filter = ('author', 'publication_year')            # Sidebar filters
    search_fields = ('title', 'author')                     # Search bar fields

admin.site.register(Book, BookAdmin)