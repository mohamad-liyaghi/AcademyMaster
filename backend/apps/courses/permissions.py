from rest_framework.permissions import BasePermission
from courses.models import Course


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
    message = 'Permission denied for updating course.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.assigned_by or request.user.has_perm(
            perm_object=Course.get_permission('change')
        )


class CanDeleteCourse(BasePermission):
    '''
    Only course assigner and managers with courses.delete_course perm
    can update unfinished courses
    '''
    message = 'Permisson denied for deleting this course.'

    def has_object_permission(self, request, view, obj):
        # TODO: Check enrollments
        return request.user == obj.assigned_by or request.user.has_perm(
            perm_object=Course.get_permission('delete')
        )
