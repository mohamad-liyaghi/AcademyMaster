from rest_framework import serializers
from courses.models import Course
from teachers.models import Teacher
from core.models import WeekDays


class CourseCreateSerializer(serializers.ModelSerializer):
    prerequisite = serializers.SlugRelatedField(
        slug_field='token',
        queryset=Course.objects.only('token'),
        required=False,
        allow_null=True
    )

    instructor = serializers.SlugRelatedField(
        slug_field='token',
        queryset=Teacher.objects.only('token')
    )
    days = serializers.MultipleChoiceField(
        choices=WeekDays.choices
    )

    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'location',
            'instructor',
            'assigned_by',
            'start_date',
            'end_date',
            'schedule',
            'days',
            'session_count',
            'prerequisite',
            'level',
            'status',
            'price',
            'token'
        ]

        extra_kwargs = {
            'assigned_by': {'read_only': True},
            'token': {'read_only': True}
        }

    def create(self, validated_data):
        # Set request.user as course assigner
        validated_data['assigned_by'] = self.context['request'].user
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValueError(str(e))
