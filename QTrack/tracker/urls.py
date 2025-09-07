from django.urls import path
from . import views


urlpatterns = [
    # Dashboard (main page for logged-in users to see overview/stats)
    path("", views.dashboard, name="dashboard"),

    # List all issues in a table format
    path("issues/", views.issue_list, name="issue_list"),

    #view my issues
    path('issues/my/', views.my_issues, name='my_issues'),

    # View details of a specific issue (by primary key / ID)
    path("<int:pk>/", views.issue_detail, name="issue_detail"),

    #create a new issue via form
    path("new/", views.issue_create, name="issue_create"),

    #assign an issue
    path("<int:pk>/assign/", views.issue_assign, name = 'issue_assign'),

    #unassigned issue
    path("unassigned/", views.unassigned_issues, name="unassigned_issues"),


    #export all issues as a CSV file (download)
    path("export/csv/", views.export_issues_csv, name="export_issues_csv"),

    #splash/landing page (separate route instead of root)
    path("home/",views.splash, name= "splash"), #homepage



    
]