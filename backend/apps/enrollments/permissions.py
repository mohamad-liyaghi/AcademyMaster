from rest_framework.permissions import BasePermission


class AllowStudentOnly(BasePermission):
    '''Allow only student to access this view'''
    def has_permission(self, request, view):
        return request.user.is_student()


class IsManagerOrObjectOwner(BasePermission):
    '''Allow only manager or object owner to access the object'''
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_manager() or
            obj.user == request.user
        )
