from django.db import models
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType


class AbstractPermission(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_subclass_permissions(cls):
        """
        Return list of all permissions for all models
        that are inherited from AbstractPermission class
        """

        # First get from cache
        permissions = cache.get('permissions')

        if not permissions:
            subclasses = AbstractPermission.__subclasses__()
            model_names = [
                subclass.__name__.lower() for subclass in subclasses
            ]
            app_labels = [
                subclass._meta.app_label for subclass in subclasses
            ]
            permissions = cls._get_permission_for_model(
                app_labels=app_labels,
                model_names=model_names
            )
            cache.set('permissions', permissions, timeout=60 * 24)

        return permissions

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

        if not permission:
            # Get from database
            try:
                permission = cls.get_subclass_permissions().get(
                    codename=codename
                )
            except Permission.DoesNotExist:
                raise ValueError("Permission not found")

            # Set cache for 24 hours and return permission
            cache.set(codename, permission, timeout=60 * 60 * 24)
        return permission

    @classmethod
    def _get_permission_for_model(cls, app_labels: list, model_names: list):
        """
        Return list of permissions for given app_labels and model_names
        Args:
            app_labels: list of app_labels
            model_names: list of model_names

        Returns: list of permissions
        """

        # Get content type ids of model
        content_type_ids = ContentType.objects.filter(
            model__in=model_names, app_label__in=app_labels
        ).values_list('id', flat=True)

        # return permissions with given content type ids
        return Permission.objects.filter(
            content_type__id__in=content_type_ids
        )

    def _validate_creator(self, creator) -> None:
        """
            Only admins and managers can promote users.
            Promoters should have the add object permission though
        """

        # admins can promote managers
        if creator.is_admin():
            return

        if not creator.is_manager():
            raise PermissionDenied("Promoter must be a manager.")

        if not creator.has_perm(
            perm_object=self.__class__.get_permission('add')
        ):
            raise PermissionDenied("Permission denied for creating.")
