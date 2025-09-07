from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Custom signup form based on CustomUser model.
    Includes email, optional username, names, password, and role selection.
    """
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "role",       # new: role selection (QA or Developer)
            "password1",
            "password2"
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-input w-full rounded-lg border-gray-300"}),
            "username": forms.TextInput(attrs={"class": "form-input w-full rounded-lg border-gray-300"}),
            "first_name": forms.TextInput(attrs={"class": "form-input w-full rounded-lg border-gray-300"}),
            "last_name": forms.TextInput(attrs={"class": "form-input w-full rounded-lg border-gray-300"}),
            "role": forms.Select(attrs={
                "class": "form-select w-full rounded-lg border-gray-300 focus:ring-2 focus:ring-blue-500"
            }),
            "password1": forms.PasswordInput(attrs={"class": "form-input w-full rounded-lg border-gray-300"}),
            "password2": forms.PasswordInput(attrs={"class": "form-input w-full rounded-lg border-gray-300"}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    """
    Override login form: replace 'username' field with email.
    """
    username = forms.EmailField(label="Email", widget=forms.EmailInput())
