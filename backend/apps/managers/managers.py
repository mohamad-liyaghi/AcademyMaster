from django.conf import settings
from django.db import models, transaction


class ManagerManager(models.Manager):

    @transaction.atomic
    def create_with_permissions(self, permissions: list = [], **kwargs):
        """
        Create an object and add permissions for the associated user.
        """
        object = self.create(**kwargs)
        if permissions:
            object.user.user_permissions.add(*permissions)
        return object

    @transaction.atomic
    def update_permission(
            self,
            user: settings.AUTH_USER_MODEL,
            permissions: list,
    ):
        """
        Update user permissions by removing all permissions of a certain class
        and adding new ones.
        """
        user.user_permissions.clear()
        if permissions:
            user.user_permissions.add(*permissions)
        return
