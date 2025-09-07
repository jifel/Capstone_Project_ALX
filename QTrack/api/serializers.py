from rest_framework import serializers
from tracker.models import Issue, Comment

# Serializer for the Comment model
class CommentSerializer(serializers.ModelSerializer):
    # Show the author's email instead of the raw user ID
    author_email = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = ['id', 'author_email', 'message', 'timestamp']
        # id: primary key of the comment
        # author_email: email of the user who wrote the comment
        # message: comment content
        # timestamp: when comment was created

# Serializer for the Issue model
class IssueSerializer(serializers.ModelSerializer):
    # Read-only fields for related users
    reporter_email = serializers.ReadOnlyField(source='reporter.email')
    assignee_email = serializers.ReadOnlyField(source='assignee.email')
    # Nested comments, read-only
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'reporter', 'reporter_email',
            'assignee', 'assignee_email',
            'created_at', 'updated_at',
            'comments',  # include all comments linked to the issue
        ]
