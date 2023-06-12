from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """
    only allow the profile owner to update it.
    """

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user)
