from rest_framework import permissions


class CanPromotePermission(permissions.BasePermission):
    """
    Only admins and managers with can_promote permission can access the page
    """

    def has_permission(self, request, view):
        user = request.user
        return (user.is_admin())\
            or (user.is_manager() and user.manager.can_promote())


class CanDemotePermission(permissions.BasePermission):
    """
    Only admins and managers with can_demote perm can access the page
    """

    def has_permission(self, request, view):
        user = request.user
        return (user.is_admin())\
            or (user.is_manager() and user.manager.can_demote())


class IsManagerPromoter(permissions.BasePermission):
    """
    Only Promoter and admins can update managers permissions
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user.is_admin())\
            or (obj.promoted_by == user)
