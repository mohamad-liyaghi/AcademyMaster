from courses.models import Course
from core.permissions import IsManager


class CanAddCourse(IsManager):
    """
    Only admins and managers with courses.add_course,
    perm can add courses
    """

    message = "You dont have permission to add course."

    def has_permission(self, request, view):
        return self._is_manager(request.user) and request.user.has_perm(
            perm_object=Course.get_permission("add")
        )


class CanUpdateCourse(IsManager):
    """
    Only managers with courses.change_course perm
    can update unfinished courses
    """

    message = "Permission denied for updating course."

    def has_object_permission(self, request, view, obj):
        return self._is_manager(request.user) and request.user.has_perm(
            perm_object=Course.get_permission("change")
        )


class CanDeleteCourse(IsManager):
    """
    Only managers with courses.delete_course perm
    can delete unfinished courses
    """

    message = "You dont have permission to delete this course."

    def has_object_permission(self, request, view, obj):
        return self._is_manager(request.user) and request.user.has_perm(
            perm_object=Course.get_permission("delete")
        )
