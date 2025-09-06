from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Register view
    path("register/", views.register, name="register"),

    # Login view
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),

    # Logout view
    path(
        "logout/",
        LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
]

urlpatterns = [
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),
]