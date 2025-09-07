from rest_framework import generics, permissions
from tracker.models import Issue
from .serializers import IssueSerializer

# Custom permission for QA/Admin vs Developers
class IsAdminOrQA(permissions.BasePermission):
    """
    Controls access based on role:
    - QA/Admin: can view, update, delete any issue
    - Developer: can view only assigned issues
    """

    def has_permission(self, request, view):
        # Any authenticated user can access list/create endpoints
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # QA/Admin can perform any action
        if request.user.role in ['qa', 'admin']:
            return True
        # Developers can only interact with issues assigned to them
        return obj.assignee == request.user

# API view to list all issues and create new issues
class IssueListCreateAPIView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()       # default queryset
    serializer_class = IssueSerializer   # serializer for JSON conversion
    permission_classes = [IsAdminOrQA]   # custom permission

    # Override to apply role-based filtering
    def get_queryset(self):
        user = self.request.user
        if user.role == 'developer':
            # Developers only see issues assigned to them
            return Issue.objects.filter(assignee=user)
        # QA/Admin see all issues
        return Issue.objects.all()

    # Automatically set the reporter when creating a new issue
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

# API view to retrieve, update, or delete a single issue
class IssueRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAdminOrQA]

    # Ensure developers cannot access issues not assigned to them
    def get_queryset(self):
        user = self.request.user
        if user.role == 'developer':
            return Issue.objects.filter(assignee=user)
        return Issue.objects.all()
