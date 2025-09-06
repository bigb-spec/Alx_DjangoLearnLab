from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login  
from django.http import HttpResponse
from django.views.generic.detail import DetailView
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

# helpers to check role
def is_admin(user):
    return hasattr(user, "profile") and user.profile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "profile") and user.profile.role == "Librarian"

def is_member(user):
    return hasattr(user, "profile") and user.profile.role == "Member"


# views for each role
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

# user registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # after registering, redirect to login
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})