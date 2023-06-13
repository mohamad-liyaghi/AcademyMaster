from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """
    Only profile owner can update its profile info.
    """

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user)


class IsNonStudent(BasePermission):
    """
    Student can only view their profiles.
    This permission doesnt accept their request for
    viewing others profile page.
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True

        return not request.user.is_student()
