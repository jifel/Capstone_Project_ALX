from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login / Logout
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='splash'), name="logout"),

    # Signup (custom view in users/views.py)
    path("signup/", views.signup_view, name="signup"),
]
