from django.db import models
from django.contrib.auth.models import Permission
from django.http import Http404


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
