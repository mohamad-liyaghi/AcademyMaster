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
