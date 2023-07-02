from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Enrollment
from courses.models import Course
from profiles.models import Profile


class EnrollmentCourseSerializer(serializers.ModelSerializer):
    '''Represent course in enrollment'''
    class Meta:
        model = Course
        fields = ('title', 'token')
        read_only_fields = ('title', 'token')


class UserProfileSerializer(serializers.ModelSerializer):
    '''Represent user profile in user serializer'''
    class Meta:
        model = Profile
        fields = [
            'avatar',
            'token'
        ]


class EnrollmentUserSerializer(serializers.ModelSerializer):
    '''Represent user in enrollment'''
    profile = serializers.SerializerMethodField(method_name='get_user_profile')

    class Meta:
        model = get_user_model()
        fields = ('full_name', 'token', 'profile')
        read_only_fields = ('full_name', 'token', 'profile')

    def get_user_profile(self, obj):
        '''
        Get user profile. Some of them might not have profile so return None
        '''
        try:
            return UserProfileSerializer(obj.profile).data
        except Exception:
            return


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field='token',
        queryset=Course.objects.only('token')
    )
    user = serializers.StringRelatedField()

    class Meta:
        model = Enrollment
        fields = ('course', 'user', 'status', 'created_at')
        read_only_fields = ('status', 'created_at', 'user')

    def create(self, validated_data):
        validated_data.update({'user': self.context['request'].user})
        try:
            return Enrollment.objects.create(**validated_data)
        except Exception as e:
            raise ValidationError(str(e))


class EnrollmentRetrieveSerializer(serializers.ModelSerializer):
    course = EnrollmentCourseSerializer()
    user = EnrollmentUserSerializer()

    class Meta:
        model = Enrollment
        fields = ('course', 'user', 'status', 'created_at')
        read_only_fields = ('course', 'user', 'status', 'created_at')


class EnrollmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('status', 'created_at')
        read_only_fields = ('created_at',)


class EnrollmentListSerializer(serializers.ModelSerializer):
    course = EnrollmentCourseSerializer()
    user = EnrollmentUserSerializer()

    class Meta:
        model = Enrollment
        fields = ('user', 'course', 'get_status_display', 'created_at')
        read_only_fields = (
            'user', 'course', 'get_status_display', 'created_at'
        )
