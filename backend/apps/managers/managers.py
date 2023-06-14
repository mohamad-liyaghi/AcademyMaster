from django.db import models
from django.contrib.auth.models import Permission
from django.conf import settings


class ManagerManager(models.Manager):

    def add_permissions(self, user: settings.AUTH_USER_MODEL, codenames: list):
        """Add the specified permissions to the user."""
        permissions = Permission.objects.filter(
            codename__in=codenames
        ).select_related("content_type")
        print(permissions)

        if permissions:
            user.user_permissions.add(*permissions)

    def remove_permissions(self, user: settings.AUTH_USER_MODEL, codenames: list):
        """Remove the specified permissions from the user."""
        permissions = Permission.objects.filter(
            codename__in=codenames
        ).select_related("content_type")

        if permissions:
            user.user_permissions.remove(*permissions)
