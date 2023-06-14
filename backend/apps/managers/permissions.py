from rest_framework import permissions


class CanPromotePermission(permissions.BasePermission):
    """
    Allow admins and managers who can promote admins
    """

    def has_permission(self, request, view):
        user = request.user
        return (user.is_admin())\
            or (user.is_manager() and user.manager.can_promote())
