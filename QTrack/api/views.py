from rest_framework import generics
from tracker.models import Issue
from .serializers import IssueSerializer
from django_filters.rest_framework import DjangoFilterBackend

# API view for listing all issues and creating new ones
# GET -> list all issues
# POST -> create a new issue
class IssueListCreateAPIView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    # enable filtering using query params like ?status=open&priority=high
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'reporter']


# API view for retrieving, updating, or deleting a single issue
# GET -> fetch one issue by ID
# PUT/PATCH -> update issue
# DELETE -> remove issue
class IssueRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

# Create your views here.
