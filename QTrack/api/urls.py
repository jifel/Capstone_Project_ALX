from django.urls import path
from .views import IssueListCreateAPIView, IssueRetrieveUpdateDestroyAPIView

urlpatterns = [
    # /api/issues/  -> list all issues (GET), create new (POST)
    path('issues/', IssueListCreateAPIView.as_view(), name='api_issue_list'),

    # /api/issues/<id>/ -> retrieve, update, delete a single issue
    path('issues/<int:pk>/', IssueRetrieveUpdateDestroyAPIView.as_view(), name='api_issue_detail'),
]
