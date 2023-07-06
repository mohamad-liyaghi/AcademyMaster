from rest_framework import serializers
from activities.models import Activity
from core.serializers import (
    CourseRelationSerializer,
    UserProfileRelationSerializer,
    EnrollmentRelationSerializer
)


class ActivityRetrieveSerializer(serializers.ModelSerializer):

    course = CourseRelationSerializer()
    user = UserProfileRelationSerializer()
    enrollment = EnrollmentRelationSerializer()

    class Meta:
        model = Activity
        fields = (
            'course',
            'user',
            'enrollment',
            'attendance',
            'final_mark',
            'created_at'
        )
        read_only_fields = fields


class ActivityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'token',
            'attendance',
            'final_mark',
        )
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))


class ActivityListSerializer(serializers.ModelSerializer):

    course = CourseRelationSerializer()
    user = UserProfileRelationSerializer()

    class Meta:
        model = Activity
        fields = (
            'course',
            'user',
            'token',
        )
        read_only_fields = fields
