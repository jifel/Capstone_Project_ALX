from django.contrib import admin

# Register your models here.
# tracker/admin.py
from django.contrib import admin
from .models import Issue, Comment

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    # Columns to show in the admin list view
    list_display = ("id", "title", "status", "priority", "reporter", "assignee", "created_at")
    # Quick filters on the right
    list_filter = ("status", "priority", "assignee", "reporter", "created_at")
    # Enable search by title/description text
    search_fields = ("title", "description")
    # Read-only fields (timestamps should not be manually edited)
    readonly_fields = ("created_at", "updated_at")
    # Default ordering in admin
    ordering = ("-created_at",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "issue", "author", "timestamp")
    list_filter = ("author", "timestamp")
    search_fields = ("message",)
    ordering = ("timestamp",)
