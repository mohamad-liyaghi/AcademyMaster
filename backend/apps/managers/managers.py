from django.conf import settings
from core.models.permissions import AbstractPermission
from django.db import models, transaction
from typing import Optional


class ManagerManager(models.Manager):

    def _get_permission_by_codename(self, codenames: str):
        return AbstractPermission.get_subclass_permissions().filter(
            codename__in=codenames
        )

    @transaction.atomic
    def create_with_permissions(
        self,
        permissions: list = [],
        codenames: Optional[str] = None,
        **kwargs
    ):
        """
        Create an object and add permissions for the associated user.
        """
        object = self.create(**kwargs)

        if codenames:
            permissions.extend(
                self._get_permission_by_codename(codenames)
            )

        if permissions:
            object.user.user_permissions.add(*permissions)

        return object

    @transaction.atomic
    def update_permission(
            self,
            user: settings.AUTH_USER_MODEL,
            permissions: Optional[list] = [],
            codenames: Optional[str] = None,
    ):
        """
        Update user permissions by removing all permissions of a certain class
        and adding new ones.
        """
        user.user_permissions.clear()
        if codenames:
            permissions.extend(self._get_permission_by_codename(codenames))

        if permissions:
            user.user_permissions.add(*permissions)
        return
