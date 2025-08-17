from django.db import models

# Create your models here.
# tracker/models.py
from django.db import models
from django.contrib.auth.models import User  # Using Django's built-in User for simplicity

class Issue(models.Model):
    """
    Represents a bug/issue reported by a user (QA).
    Core fields support filtering/search and a simple workflow.
    """

    # Priority options shown in forms/admin; stored as lowercase strings
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # Status workflow for the issue lifecycle
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    # Short, human-friendly summary
    title = models.CharField(max_length=200)

    # Detailed description of the problem, steps to reproduce, expected vs actual, etc.
    description = models.TextField()

    # Priority helps triage; db_index=True to speed up filtering in lists
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='low',
        db_index=True,  # helpful for list filters
    )

    # Current state in the workflow; also indexed for faster queries
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        db_index=True,
    )

    # Who reported the issue (QA). If the user is deleted, delete their issues too.
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reported_issues",
    )

    # Which developer is assigned (optional). If the user is deleted, keep the issue but set to NULL.
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues",
    )

    # Auto-managed timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # set once on create
    updated_at = models.DateTimeField(auto_now=True)      # update on every save

    class Meta:
        # Default ordering: newest issues first
        ordering = ["-created_at"]
        # Useful combined index for list pages with filters/sorts
        indexes = [
            models.Index(fields=["status", "priority"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        # Nice string in admin/lists
        return f"{self.title} [{self.get_status_display()}]"


class Comment(models.Model):
    """
    Internal thread/message on an Issue (like a ticket conversation).
    """

    # Link to the parent Issue; delete comments if the Issue is deleted
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    # Who wrote the comment
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    # The message content
    message = models.TextField()

    # When this comment was created
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Oldest first reads like a conversation; adjust to ["-timestamp"] if you prefer newest first
        ordering = ["timestamp"]
        indexes = [
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title}"
