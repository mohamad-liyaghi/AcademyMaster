from core.permissions import IsNonStudent, IsObjectOwner


class CanUpdateProfile(IsObjectOwner):
    """
    Only profile owner can update profile.
    """

    message = "Only profile owner can perform this action."

    def has_object_permission(self, request, view, obj):
        user = request.user
        return self._is_object_owner(user, obj)


class CanRetrieveProfile(IsNonStudent, IsObjectOwner):
    """
    Only non-students such as admin/manager/teacher and the profile owner
    can retrieve profile.
    """

    message = "Only non-students and profile owner can perform this action."

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        return self._is_object_owner(user, obj) or self._is_non_student(user)
