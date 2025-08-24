from django.urls import path
from . import views


urlpatterns = [

    path("", views.dashboard, name="dashboard"),
    path("issues/", views.issue_list, name="issue_list"),
    path("issues/<int:pk>/", views.issue_detail, name="issue_detail"),
    path("issues/new/", views.issue_create, name="issue_create"),
    
]