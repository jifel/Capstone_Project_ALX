# users/views.py
from django.contrib.auth.forms import UserCreationForm  # Django's built-in signup form
from django.shortcuts import render, redirect

def signup(request):
    """
    User Signup View:
    - Handles user registration.
    - On GET: displays a blank signup form.
    - On POST: validates and creates a new user.
    - After successful signup, redirects to splash page (for login).
    """
    if request.method == "POST":
        # Bind submitted form data to UserCreationForm
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save new user to database
            form.save()
            # Redirect back to splash page for login
            return redirect("splash")
    else:
        # If GET request, show empty signup form
        form = UserCreationForm()

    # Render signup template with form
    return render(request, "registration/signup.html", {"form": form})
