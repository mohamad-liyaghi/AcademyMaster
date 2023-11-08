from core.permissions import IsStudent, IsManager, IsObjectOwner


class CanRetrieveEnrollment(IsObjectOwner, IsManager, IsStudent):
    """Allow only managers and object owner to access the object"""

    message = "Only object owner can access this object"

    def has_permission(self, request, view):
        return self._is_manager(request.user) or self._is_student(request.user)

    def has_object_permission(self, request, view, obj):
        return self._is_manager(request.user) or self._is_object_owner(
            request.user, obj
        )
