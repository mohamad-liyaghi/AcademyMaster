from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import serializers
from courses.models import Course
from profiles.models import Profile
from teachers.models import Teacher
from enrollments.models import Enrollment


class PermissionSerializer(serializers.ModelSerializer):
    '''Represent permission codenames'''
    class Meta:
        model = Permission
        fields = ['codename']


class UserRelationSerializer(serializers.ModelSerializer):
    '''Represend user in relations'''

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class ProfileRelationSerializer(serializers.ModelSerializer):
    '''Represent base profile in relation fields'''
    class Meta:
        model = Profile
        fields = (
            'avatar',
            'birth_date',
            'token',
        )


class UserProfileRelationSerializer(UserRelationSerializer):
    '''Represent user/profile in relation fields'''
    profile = ProfileRelationSerializer()

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'email',
            'profile'
        )

    def get_user_profile(self, user):
        '''
            Return user profile
            Some users may not have a profile, so return None
        '''
        try:
            return user.profile

        except Exception:
            return None


class InstructorRelationSerializer(serializers.ModelSerializer):
    '''Represent course instructor in relations'''
    user = UserRelationSerializer()

    class Meta:
        model = Teacher
        fields = (
            'user',
            'token',
        )


class CourseRelationSerializer(serializers.ModelSerializer):
    '''Represent course basic info in in relations'''
    class Meta:
        model = Course
        fields = (
            'title',
            'token',
        )


class EnrollmentRelationSerializer(serializers.ModelSerializer):
    '''Represent enrollment base info in relations'''
    class Meta:
        model = Enrollment
        fields = ('created_at', 'get_status_display', 'token')
