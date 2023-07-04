from rest_framework.permissions import BasePermission


class CanRetrieveActivity(BasePermission):
    '''Non students and the activity's owner can retrieve the activity'''

    message = 'You do not have permission to retrieve this activity'

    def has_object_permission(self, request, view, obj):
        user = request.user
        return not user.is_student() or user == obj.user


class CanUpdateActivity(BasePermission):
    '''Only the course instructor can update the activity'''
    message = 'You do not have permission to update this activity'

    def has_object_permission(self, request, view, obj):
        return obj.course.instructor.user == request.user
