from rest_framework.permissions import BasePermission
from managers.models import Manager


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manager()


class CanAddManager(BasePermission):
    """
    Only admins and managers with can_promote permission can access the page
    """
    message = 'You cannot promote managers.'

    def has_permission(self, request, view):
        return request.user.has_perm(
            perm_object=Manager.get_permission('add')
        )


class CanDeleteManager(BasePermission):
    """
    Only admins and managers with can_demote perm can access the page
    """

    message = 'You cannot delete this manager.'

    def has_permission(self, request, view):
        return request.user.has_perm(
            perm_object=Manager.get_permission('delete')
        )


class CanChangeManager(BasePermission):
    """
    Only Promoter and admins can update managers permissions
    """
    message = 'You cannot update this manager.'

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm(
            perm_object=Manager.get_permission('change')
        )
