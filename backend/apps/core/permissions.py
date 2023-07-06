from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    '''Check if user is manager'''
    message = 'Only managers can perform this action.'

    def has_permission(self, request, view):
        return self._is_manager(request.user)

    def _is_manager(self, user):
        return user.is_manager()


class IsTeacher(BasePermission):
    '''Check if user is teacher'''
    message = 'Only teachers can perform this action.'

    def has_permission(self, request, view):
        return self._is_teacher(request.user)

    def _is_teacher(self, user):
        return user.is_teacher()


class IsStudent(BasePermission):
    '''Check if user is student'''
    message = 'Only students can perform this action.'

    def has_permission(self, request, view):
        return self._is_student(request.user)

    def _is_student(self, user):
        return user.is_student()


class IsNonStudent(BasePermission):
    '''Check if user is non-student'''
    message = 'Only non-students can perform this action.'

    def has_permission(self, request, view):
        return self._is_non_student(request.user)

    def _is_non_student(self, user):
        return not user.is_student()


class IsObjectOwner(BasePermission):
    '''Check if user is object owner'''
    message = 'Only object owner can perform this action.'

    def has_object_permission(self, request, view, obj):
        return self._is_object_owner(request.user, obj)

    def _is_object_owner(self, user, obj):
        return (obj.user == user)
