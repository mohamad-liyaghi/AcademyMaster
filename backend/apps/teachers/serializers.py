from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from teachers.models import Teacher
from django.contrib.auth import get_user_model


class TeacherCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='token',
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Teacher
        fields = [
            'user',
            'token'
        ]
        extra_kwargs = {
            'token': {'read_only': True}
        }

    def create(self, validated_data):
        user = validated_data['user']

        # Raise error for promoting admins/managers
        if not user.is_student():
            raise ValidationError('You cannot promote non-student users.')

        teacher = Teacher.objects.create(
            user=user,
            promoted_by=self.context['request'].user,
        )

        return teacher
