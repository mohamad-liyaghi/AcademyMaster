from django.db import models
from django.contrib.auth.models import Permission
from django.http import Http404
from django.core.exceptions import ValidationError


class AbstractPermission(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_permission(cls, action):
        '''
        Return a permission related to a class
        '''
        codename = f'{action}_{cls.__name__.lower()}'

        try:
            return Permission.objects.get(codename=codename)

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

        if not self.promoted_by.has_perm(
            perm_object=self.__class__.get_permission('add')
        ):
            raise ValidationError("Permission denied for promoting.")
