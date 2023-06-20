from rest_framework.permissions import BasePermission
from teachers.models import Teacher


class CanAddTeacher(BasePermission):
    '''
    Only admins and managers with teachers.add_teacher,
    perm can promote teachers
    '''
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_manager() and user.has_perm(
                Teacher.get_permission('add', return_str=True)
            )
        )


class CanDeleteTeacher(BasePermission):
    '''
    Only admins and managers with teachers.delete_teacher,
    perm can delete teachers
    '''
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_manager() and user.has_perm(
                Teacher.get_permission('delete', return_str=True)
            )
        )


class IsObjectOwner(BasePermission):
    '''
    Only teacher object owner can update the object
    '''
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
