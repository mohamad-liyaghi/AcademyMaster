from rest_framework.permissions import BasePermission


class AllowStudentOnly(BasePermission):
    '''Allow only student to access this view'''
    message = 'Only student can access this page'

    def has_permission(self, request, view):
        return request.user.is_student()


class IsManagerOrStudent(BasePermission):
    '''Allow only manager and student to access the page'''
    message = 'Only manager and student can access this page'

    def has_permission(self, request, view):
        return request.user.is_manager() or request.user.is_student()


class IsObjectOwner(BasePermission):
    '''Allow only managers and object owner to access the object'''
    message = 'Only object owner can access this object'

    def has_object_permission(self, request, view, obj):
        return request.user.is_manager() or obj.user == request.user
