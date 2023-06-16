from django.db import models, transaction
from django.contrib.auth.models import Permission
from django.conf import settings


class BasePermissionManager(models.Manager):
    """
    Custom manager for managing user permissions.
    """

    @transaction.atomic
    def create_with_permissions(self, permissions: list = [], **kwargs):
        """
        Create an object and add permissions for the associated user.
        """
        object = self.create(**kwargs)
        if permissions:
            self.add_permissions(
                user=object.user,
                permissions=permissions
            )
        return object

    def add_permissions(
            self,
            user: settings.AUTH_USER_MODEL,
            permissions: list
    ) -> None:
        """
        Add permissions for a user.
        """
        # Filter the permissions by their codenames
        permissions = Permission.objects.filter(
            codename__in=permissions
        ).select_related("content_type")

        if permissions:
            # Add the filtered permissions to the user's permission set
            user.user_permissions.add(*permissions)

    def remove_permissions(
            self,
            user: settings.AUTH_USER_MODEL,
            permissions: list
    ) -> None:
        """
        Remove the specified permissions from the user.
        """
        # Filter the permissions by their codenames
        permissions = Permission.objects.filter(
            codename__in=permissions
        ).select_related("content_type")

        if permissions:
            # Remove the filtered permissions from the user's permission set
            user.user_permissions.remove(*permissions)

    @transaction.atomic
    def update_permission(
            self,
            user: settings.AUTH_USER_MODEL,
            permissions: list,
            permission_class
    ):
        """
        Update user permissions by removing all permissions of a certain class
        and adding new ones.
        """
        if permissions:
            self.remove_all_permissions(
                user=user,
                permission_class=permission_class
            )
            self.add_permissions(
                user=user,
                permissions=permissions
            )
        return

    @transaction.atomic
    def remove_all_permissions(
            self,
            user: settings.AUTH_USER_MODEL,
            permission_class
    ):
        """
        Remove all permissions of a certain class
        from the user's permission set.
        """
        self.remove_permissions(
                user=user,
                permissions=[*permission_class]
        )

    def has_permission(
            self,
            user: settings.AUTH_USER_MODEL,
            permission: str
    ):
        """
        Check if the user has a specific permission.
        """
        return user.user_permissions.filter(
            codename=permission
        ).exists()

    def get_permission_list(
            self,
            user: settings.AUTH_USER_MODEL,
            permission_class
    ):
        """
        Get all permissions of a user from a certain class.
        """
        codenames = [choice.value for choice in permission_class]
        return user.user_permissions.filter(
            codename__in=codenames
        )
