from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from .forms import AssignIssueForm
from .models import Issue
from .forms import IssueForm
import csv
from django.http import HttpResponse


@login_required
def issue_list(request):
    """
    Issue list view with strict role filtering:
    - QA/Admin (role='qa' or superuser) see all issues (with optional filters)
    - Developers (role='dev') see only issues assigned to them
    """
    user_role = getattr(request.user, "role", "").lower()
    
    # Developers: only assigned issues
    if user_role == "dev":
        issues = Issue.objects.filter(assignee=request.user)
    else:
        # QA/Admin: all issues with optional filters
        issues = Issue.objects.all()
        
        # Apply filters
        status = request.GET.get("status")
        priority = request.GET.get("priority")
        reporter = request.GET.get("reporter")
        assigned = request.GET.get("assigned")

        if status:
            issues = issues.filter(status=status)
        if priority:
            issues = issues.filter(priority=priority)
        if reporter:
            issues = issues.filter(reporter__username__icontains=reporter)
        if assigned == "yes":
            issues = issues.exclude(assignee__isnull=True)
        elif assigned == "no":
            issues = issues.filter(assignee__isnull=True)

    context = {
        "issues": issues,
        "user_role": user_role,  # used in template to control buttons/filters
    }
    return render(request, "tracker/issue_list.html", context)


#view to show details of one issue
def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)

    # Check role or group membership in Python (cleaner than template logic)
    is_qa = (
        getattr(request.user, "role", None) in ["qa", "admin"]
        or request.user.groups.filter(name__in=["QA", "Admin"]).exists()
    )

    return render(
        request,
        "tracker/issue_detail.html",
        {"issue": issue, "is_qa": is_qa}
    )



#view to create a new issue
@login_required
def issue_create(request):
    #allow only QA/Admin roles
    if request.user.role not in ["qa", "admin"] and not request.user.groups.filter(
        name__in=["QA", "Admin"]
    ).exists():
        raise PermissionDenied("You are not allowed to create issues.")
    
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
@login_required
def dashboard(request):
    """
    Show summary stats for issues.
    - QA/Admins see all issues
    - Developers see only issues assigned to them
    """
    user_role = getattr(request.user, "role", "").lower()

    if user_role in ["qa", "admin"]:
        issues = Issue.objects.all()
    else:
        issues = Issue.objects.filter(assignee=request.user)

    context = {
        "total_issues": issues.count(),
        "open_issues": issues.filter(status="open").count(),
        "closed_issues": issues.filter(status="closed").count(),
        "user_role": user_role,  # pass role to template for quick actions
    }
    return render(request, "tracker/dashboard.html", context)



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


# view to assign issue

@login_required
def issue_assign(request, pk):
    """
    Allow only QA/Admins to assign an issue to a developer.
    Developers should not access this.
    """
    issue = get_object_or_404(Issue, pk=pk)

    # Only QA/Admins can assign
    if request.user.role not in ["qa", "admin"] and not request.user.groups.filter(name__in=["QA", "Admin"]).exists():
        raise PermissionDenied("You are not allowed to assign issues.")

    if request.method == "POST":
        form = AssignIssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            #redirect to unassigned issues list after assigning
            return redirect("unassigned_issues")
    else:
        form = AssignIssueForm(instance=issue)

    return render(request, "tracker/assign_issue.html", {"form": form, "issue": issue})

#view for filtered unassigned issues
@login_required
def unassigned_issues(request):
    """Show only unassigned issues for QA/Admins."""
    issues = Issue.objects.filter(assignee__isnull=True)

    context = {
        "issues": issues,
    }
    return render(request, "tracker/unassigned_issues.html", context)

@login_required
def my_issues(request):
    
    return redirect('issue_list')



