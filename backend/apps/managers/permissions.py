from rest_framework import permissions


class CanPromotePermission(permissions.BasePermission):
    """
    Allow admins and managers who can promote admins
    """

    def has_permission(self, request, view):
        user = request.user
        return (user.is_admin())\
            or (user.is_manager() and user.manager.can_promote())


class IsManagerPromoter(permissions.BasePermission):
    """
    Only Promoter and admins can update managers permissions
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user.is_admin())\
            or (obj.promoted_by == user)
