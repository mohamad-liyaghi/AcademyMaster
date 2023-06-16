from rest_framework import permissions
from managers.models import Manager, ManagerPermission


class BaseIsAdminOrManager(permissions.BasePermission):
    def is_admin_or_manager(self, user):
        return user.is_admin() or user.is_manager()


class IsManager(BaseIsAdminOrManager):
    def has_permission(self, request, view):
        return self.is_admin_or_manager(request.user)


class CanPromotePermission(BaseIsAdminOrManager):
    """
    Only admins and managers with can_promote permission can access the page
    """

    def has_permission(self, request, view):
        user = request.user
        return self.is_admin_or_manager(user) and (
            user.is_admin() or
            Manager.objects.has_permission(
                user=user,
                permission=ManagerPermission.PROMOTE.value
            )
        )


class CanDemotePermission(BaseIsAdminOrManager):
    """
    Only admins and managers with can_demote perm can access the page
    """

    def has_permission(self, request, view):
        user = request.user
        return self.is_admin_or_manager(user) and (
            user.is_admin() or
            Manager.objects.has_permission(
                user=user,
                permission=ManagerPermission.DEMOTE.value
            )
        )


class IsManagerPromoter(BaseIsAdminOrManager):
    """
    Only Promoter and admins can update managers permissions
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        return self.is_admin_or_manager(user) and (
            user.is_admin() or obj.promoted_by == user
        )
