from django.urls import path
from .views import IssueListCreateAPIView, IssueRetrieveUpdateDestroyAPIView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # /api/issues/  -> list all issues (GET), create new (POST)
    path('issues/', IssueListCreateAPIView.as_view(), name='api_issue_list'),

     # Token login endpoint
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # /api/issues/<id>/ -> retrieve, update, delete a single issue
    path('issues/<int:pk>/', IssueRetrieveUpdateDestroyAPIView.as_view(), name='api_issue_detail'),
]
