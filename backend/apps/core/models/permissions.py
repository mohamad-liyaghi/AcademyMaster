from django.db import models
from django.contrib.auth.models import Permission
from django.http import Http404
from django.core.exceptions import ValidationError


class AbstractPermission(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_permission(cls, action, return_str=False):
        '''
        Return a permission related to a class
        :return_str: return the codename or the object
        '''
        codename = f'{action}_{cls.__name__.lower()}'

        try:
            permission = Permission.objects.get(codename=codename)
            if return_str:
                return f'{cls._meta.app_label}.{codename}'

            return permission

        except Http404:
            raise ValueError("Permission not fount")

    def _validate_promoter(self) -> None:
        '''
            Only admins and managers can promote users.
            Promoters should have the add object permission though
        '''

        # admins can promote managers
        if self.promoted_by.is_admin():
            return

        if not self.promoted_by.is_manager():
            raise ValidationError("Promoter must be a manager.")

        if not self.promoted_by.user_permissions.filter(
            codename=self.__class__.get_permission('add').codename
        ):
            raise ValidationError("Permission denied for promoting.")
