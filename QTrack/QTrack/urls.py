"""
URL configuration for QTrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tracker import views   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('issues/', include('tracker.urls')), #include tracker app routes (issues, etc)
    path('accounts/', include('users.urls')), # include users app routes (authentication, profiles)
    path('api/', include('api.urls')), # for exposing the api endpoints


    #root routes
    path("", views.splash, name="splash"), #splash page for logout
    path("dashboard/", views.dashboard, name="dashboard"), #dashboard after login
]
