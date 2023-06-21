from rest_framework.permissions import BasePermission
from managers.models import Manager


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manager()


class CanPromotePermission(BasePermission):
    """
    Only admins and managers with can_promote permission can access the page
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_manager() and
            user.has_perm(perm_object=Manager.get_permission('add'))
        )


class CanDemotePermission(BasePermission):
    """
    Only admins and managers with can_demote perm can access the page
    """

    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_manager() and
            user.has_perm(perm_object=Manager.get_permission('delete'))
        )


class IsManagerPromoter(BasePermission):
    """
    Only Promoter and admins can update managers permissions
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_admin() or
            user.is_manager() and obj.promoted_by == user
        )
