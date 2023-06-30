from django.db import models
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.cache import cache


class AbstractPermission(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_permission(cls, action):
        """
        Return a permission object related to the given action and model class.

        The permission object name is constructed by appending
        the given action to the class name in lowercase.

        Examples:
        get_permission('add', Course) -> add_course permission
        """
        codename = f'{action}_{cls.__name__.lower()}'

        # Check cache first
        permission = cache.get(codename)

        if permission:
            return permission

        # Get from database
        try:
            permission = Permission.objects.get(codename=codename)
        except Permission.DoesNotExist:
            raise ValueError("Permission not found")

        # Set cache for 24 hours and return permission
        cache.set(codename, permission, timeout=60 * 60 * 24)
        return permission

    def _validate_creator(self, creator) -> None:
        '''
            Only admins and managers can promote users.
            Promoters should have the add object permission though
        '''

        # admins can promote managers
        if creator.is_admin():
            return

        if not creator.is_manager():
            raise ValidationError("Promoter must be a manager.")

        if not creator.has_perm(
            perm_object=self.__class__.get_permission('add')
        ):
            raise ValidationError("Permission denied for creating.")
