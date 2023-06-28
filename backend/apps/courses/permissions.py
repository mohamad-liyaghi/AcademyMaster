from rest_framework.permissions import BasePermission
from courses.models import Course, CourseStatus


class CanAddCourse(BasePermission):
    '''
    Only admins and managers with courses.add_course,
    perm can add courses
    '''
    message = 'You dont have permission to add course.'

    def has_permission(self, request, view):
        return request.user.has_perm(
            perm_object=Course.get_permission('add')
        )


class CourseStatusPermission(BasePermission):
    def _is_completed(self, obj):
        return (obj.status == CourseStatus.COMPLETED)


class CanUpdateCourse(CourseStatusPermission):
    '''
    Only course assigner and managers with courses.change_course perm
    can update unfinished courses
    '''
    message = 'You cannot update this course.'

    def has_object_permission(self, request, view, obj):
        # Check object status is Completed
        if self._is_completed(obj=obj):
            self.message = 'You cannot update a completed course'
            return False

        return request.user == obj.assigned_by or request.user.has_perm(
            perm_object=Course.get_permission('change')
        )


class CanDeleteCourse(CourseStatusPermission):
    '''
    Only course assigner and managers with courses.delete_course perm
    can update unfinished courses
    '''
    message = 'You cannot delete this course.'

    def has_object_permission(self, request, view, obj):
        # TODO: Check enrollments

        # Check object status is Completed
        if self._is_completed(obj=obj):
            self.message = 'You cannot delete a completed course'
            return False

        return request.user == obj.assigned_by or request.user.has_perm(
            perm_object=Course.get_permission('delete')
        )
