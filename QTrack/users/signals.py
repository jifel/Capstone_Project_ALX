# users/signals.py
from django.db.models.signals import post_migrate, post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# 1) Ensure groups exist after migrations run
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Create QA Agent and Developer groups if they don't exist.
    Also attach the can_assign_issue permission to QA Agent.
    """
    qa_group, _ = Group.objects.get_or_create(name="QA Agent")
    dev_group, _ = Group.objects.get_or_create(name="Developer")
    admin_group, _ = Group.objects.get_or_create(name="Admin")

    # Try to attach 'can_assign_issue' permission to QA Agent.
    try:
        assign_perm = Permission.objects.get(codename="can_assign_issue")
        qa_group.permissions.add(assign_perm)
    except Permission.DoesNotExist:
        # It's okay if the permission doesn't exist yet (will be created later by migrations).
        pass


# 2) Sync role → group when a CustomUser is saved
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def sync_user_groups(sender, instance, **kwargs):
    """
    When a user is created/updated, assign them to a group based on instance.role.
    This ensures role->group sync so we can use Django's permission system.
    """
    if not instance.role:
        return

    role_to_group = {
        "qa": "QA Agent",
        "developer": "Developer",
        "admin": "Admin",
    }
    group_name = role_to_group.get(instance.role.lower())

    if not group_name:
        return

    group, _ = Group.objects.get_or_create(name=group_name)
    # Replace the user's groups with only this role's group
    instance.groups.set([group])


# 3) Sync group → role when groups are changed in the admin
@receiver(m2m_changed, sender=User.groups.through)
def sync_group_to_role(sender, instance, action, **kwargs):
    """
    Keep user.role in sync if groups are changed manually from the admin.
    Runs when a user's groups are updated.
    """
    if action in ["post_add", "post_remove", "post_clear"]:
        groups = instance.groups.values_list("name", flat=True)

        # Map group names back to roles
        group_to_role = {
            "QA Agent": "qa",
            "Developer": "developer",
            "Admin": "admin",
        }

        intersection = [g for g in groups if g in group_to_role]

        if len(intersection) == 1:
            # Update role field to match group
            instance.role = group_to_role[intersection[0]]
            instance.save(update_fields=["role"])
