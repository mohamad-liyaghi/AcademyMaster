from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Enrollment
from courses.models import Course


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field='token',
        queryset=Course.objects.only('token')
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ('course', 'user', 'status', 'created_at')
        read_only_fields = ('status', 'created_at')

    def create(self, validated_data):
        validated_data.update({'user': self.context['request'].user})
        try:
            return Enrollment.objects.create(**validated_data)
        except Exception as e:
            raise ValidationError(str(e))
