from django import forms
from .models import Issue

#form view(create issue) - add new issues from the browser
class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'priority']


        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs.update({"class": "form-control"})