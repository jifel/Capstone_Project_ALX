from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Issue
from .forms import IssueForm


#view to list all issues
def issue_list(request):
    issues = Issue.objects.all()
    return render(request, 'tracker/issue_list.html',{"issues": issues})

#view to show details of one issue
def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    return render(request, 'tracker/issue_detail.html', {'issue': issue})


#view to create a new issue
@login_required
def issue_create(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False) #dont save yet
            issue.reporter = request.user # set the reporter
            issue.save()
            return redirect('issue_list')

    else:
        form = IssueForm()
    return render(request, 'tracker/issue_form.html',{'form': form})    

#dashboard view - show summary stats(total issues, open issues, closed issues)
def dashboard(request):
    total_issues = Issue.objects.count()
    open_issues = Issue.objects.filter(status='open').count()
    closed_issues = Issue.objects.filter(status='closed').count()

    context = {
        'total_issues': total_issues,
        'open_issues': open_issues,
        'closed_issues': closed_issues,
    }

    return render(request, 'tracker/dashboard.html', context)