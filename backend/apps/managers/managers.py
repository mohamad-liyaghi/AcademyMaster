from django.conf import settings
from typing import List
from managers.models.permission import ManagerPermission
from core.managers import BasePermissionManager


class ManagerManager(BasePermissionManager):
    """
    Custom manager for managing Manager objects and permissions.
    Inherits from BasePermissionManager to provide permission-related methods.
    """

    def create_with_permissions(
            self,
            permissions: List[ManagerPermission] = [],
            **kwargs
    ):
        """
        Create a new Manager object
        and add permissions for the associated user.
        """
        return super().create_with_permissions(permissions, **kwargs)

    def update_permission(
            self,
            user: settings.AUTH_USER_MODEL,
            permissions: List[ManagerPermission],
            permission_class: ManagerPermission = ManagerPermission
    ):
        """
        Update a Manager's permissions by removing all permissions
        of a certain classand adding new ones.
        """
        return super().update_permission(user, permissions, permission_class)

    def add_permissions(
            self,
            user: settings.AUTH_USER_MODEL,
            permissions: List[ManagerPermission]
    ):
        """
        Add permissions for a Manager.
        """
        return super().add_permissions(user, permissions)

    def remove_permissions(
            self,
            user: settings.AUTH_USER_MODEL,
            permissions: List[ManagerPermission]
    ):
        """
        Remove permissions from a Manager.
        """
        return super().remove_permissions(user, permissions)

    def remove_all_permissions(
            self,
            user: settings.AUTH_USER_MODEL,
            permission_class: ManagerPermission = ManagerPermission
    ):
        """
        Remove all permissions of a certain class
        from a Manager's permission set.
        """
        return super().remove_all_permissions(user, permission_class)

    def has_permission(
            self,
            user: settings.AUTH_USER_MODEL,
            permission: str
    ):
        """
        Check if a Manager has a specific permission.
        """
        return super().has_permission(user, permission)

    def get_permission_list(
            self,
            user: settings.AUTH_USER_MODEL,
            permission_class: ManagerPermission = ManagerPermission
    ):
        """
        Get all permissions of a Manager from a certain class.
        """
        return super().get_permission_list(user, permission_class)
