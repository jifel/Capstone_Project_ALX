from django import forms
from .models import Issue

#form view(create issue) - add new issues from the browser
class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'priority']
