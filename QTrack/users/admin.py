from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin user list
    list_display = ("email", "username", "first_name", "last_name", "is_staff", "is_active", "role")

    # Fields to filter by in the sidebar
    list_filter = ("is_staff", "is_active", "is_superuser")

    # Fieldsets for editing a user (grouping in admin UI)
    fieldsets = (
        (None, {"fields": ("email", "username", "password", "role")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fieldsets for creating a new user (when using “Add user” in admin)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    # Use email as the identifier for searching
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)


# Register the custom user model with its admin
admin.site.register(CustomUser, CustomUserAdmin)
