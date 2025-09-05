from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model that extends Django's AbstractUser

class CustomUser(AbstractUser):
    #make email required + unique (default abstractuser allows duplicates)
    email = models.EmailField(unique=True)

    #keep username as unique too but optional at signup
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    #Tell django to use email as the primary login field
    USERNAME_FIELD = 'email'

    #Extra fields required when creating a superuser via 'createsuperuser'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        #display email when printing user object
        return self.email
