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


class CanUpdateCourse(BasePermission):
    '''
    Only course assigner and managers with courses.change_course perm
    can update unfinished courses
    '''
    message = 'You cannot update this course.'

    def has_object_permission(self, request, view, obj):
        if obj.status == CourseStatus.COMPLETED:
            self.message = 'You cannot update complete courses'
            return False

        return request.user == obj.assigned_by or request.user.has_perm(
            perm_object=Course.get_permission('change')
        )
