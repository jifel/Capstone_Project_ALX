from django import forms
from .models import Issue, Comment
from django.conf import settings
from django.contrib.auth import get_user_model 

#form view(create issue) - add new issues from the browser
class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'priority']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})



class AssignIssueForm(forms.ModelForm):
    """
    Form for QA/Admins to assign issues to Developers.
    Works with both:
      - CustomUser.role field (role="developer")
      - Django Groups (users in 'Developer' group)
    """

    class Meta:
        model = Issue
        fields = ['assignee']
        widgets = {
            'assignee': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()

        # Developers from both systems
        role_based = User.objects.filter(role="developer").values_list("id", flat=True)
        group_based = User.objects.filter(groups__name="Developer").values_list("id", flat=True)

        # Merge and deduplicate IDs
        dev_ids = set(role_based) | set(group_based)

        # If no developers found, fall back gracefully
        if dev_ids:
            self.fields['assignee'].queryset = User.objects.filter(id__in=dev_ids)
        else:
            self.fields['assignee'].queryset = User.objects.none()


#form view to add comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Add your comment here..."
            }),
        }
        labels = {
            "message": ""
        }