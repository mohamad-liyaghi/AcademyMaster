from core.permissions import IsManager, IsObjectOwner
from teachers.models import Teacher


class CanAddTeacher(IsManager):
    """
    Only managers with teachers.add_teacher perm can promote teachers
    """

    message = "You dont have permission to add teacher"

    def has_permission(self, request, view):
        return self._is_manager(request.user) and request.user.has_perm(
            perm_object=Teacher.get_permission("add")
        )


class CanDeleteTeacher(IsManager):
    """
    Only admins and managers with teachers.delete_teacher,
    perm can delete teachers
    """

    message = "You dont have permission to delete teacher"

    def has_permission(self, request, view):
        return self._is_manager(request.user) and request.user.has_perm(
            perm_object=Teacher.get_permission("delete")
        )


class CanUpdateTeacher(IsObjectOwner):
    """
    Only teacher object owner can update the object
    """

    def has_object_permission(self, request, view, obj):
        return self._is_object_owner(request.user, obj)
