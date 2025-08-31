from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login
from .models import Issue
from .forms import IssueForm
import csv
from django.http import HttpResponse


#view to list all issues
def issue_list(request):
    """
    Show list of issues in HTML, with filtering options.
    Filters mimic API filter fields for consistency.
    """
    issues = Issue.objects.all()

    # Get filter parameters from the request
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    reporter = request.GET.get('reporter')  # optional filter by reporter

    # Apply filters if provided
    if status:
        issues = issues.filter(status=status)
    if priority:
        issues = issues.filter(priority=priority)
    if reporter:
        issues = issues.filter(reporter__username__icontains=reporter)

    return render(request, 'tracker/issue_list.html', {"issues": issues})

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




# View to export all issues into a CSV file
def export_issues_csv(request):
    # Create an HTTP response object with the content type set to CSV
    response = HttpResponse(content_type='text/csv')

    # Set the response headers to force a download with the filename "issues.csv"
    response['Content-Disposition'] = 'attachment; filename="issues.csv"'

    # Create a CSV writer object, writing directly to the response
    writer = csv.writer(response)

    # Write the header row (column names)
    writer.writerow(['ID', 'Title', 'Description', 'Status', 'Priority', 'Reporter', 'Created At'])

    # Loop through all issues in the database
    for issue in Issue.objects.all():
        # Write each issue's data as a row in the CSV
        writer.writerow([
            issue.id,                           # Issue ID
            issue.title,                        # Title of the issue
            issue.description,                  # Description text
            issue.status,                       # Current status (e.g., open, closed)
            issue.priority,                     # Priority level
            issue.reporter.username if issue.reporter else "",  # Reporter username (if exists)
            issue.created_at,                   # Date issue was created
        ])

    # Return the response, which is now a downloadable CSV file
    return response

#view for splash ppage
def splash(request):
    """
    Splash (Landing) Page:
    - Serves as the login page + entry splash.
    - If the user is already logged in, redirect them to the dashboard.
    - Otherwise, display the login form.
    """
    # If user is already logged in, skip splash and go directly to dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")

    # Initialize the login form (AuthenticationForm)
    # If POST request, bind submitted data, else create an empty form
    form = AuthenticationForm(request, data=request.POST or None)

    # Handle form submission (when user clicks "Log In")
    if request.method == "POST":
        if form.is_valid():
            # Retrieve the authenticated user from the form
            user = form.get_user()
            # Log the user in (create session)
            login(request, user)
            # Redirect to dashboard after successful login
            return redirect("dashboard")

    # Render the splash page with login form (GET request or invalid form)
    return render(request, "tracker/splash.html", {"form": form})