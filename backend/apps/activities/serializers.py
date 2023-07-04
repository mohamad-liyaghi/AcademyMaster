from rest_framework import serializers
from activities.models import Activity


# TODO make serializers for course/user/enroll
class ActivityRetrieveSerializer(serializers.ModelSerializer):

    course = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    enrollment = serializers.StringRelatedField()

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
