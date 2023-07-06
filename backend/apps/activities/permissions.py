from rest_framework.permissions import BasePermission
from core.permissions import IsObjectOwner, IsNonStudent


class CanRetrieveActivity(IsObjectOwner, IsNonStudent):
    '''Non students and the activity's owner can retrieve the activity'''

    message = 'You do not have permission to retrieve this activity'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
                self._is_object_owner(user=user, obj=obj) or
                self._is_non_student(request.user)
            )


class CanUpdateActivity(BasePermission):
    '''Only the course instructor can update the activity'''
    message = 'You do not have permission to update this activity'

    def has_object_permission(self, request, view, obj):
        return obj.course.instructor.user == request.user


class IsCourseInstructor(BasePermission):
    '''Only the course instructor can retrieve activities of a course'''
    message = 'You dont have permission to retrieve activities of this course'

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_manager() or
            obj.instructor.user == request.user
        )
