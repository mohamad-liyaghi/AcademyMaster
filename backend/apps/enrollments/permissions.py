from rest_framework.permissions import BasePermission


class AllowStudentOnly(BasePermission):
    '''Allow only student to access this view'''
    def has_permission(self, request, view):
        return request.user.is_student()
