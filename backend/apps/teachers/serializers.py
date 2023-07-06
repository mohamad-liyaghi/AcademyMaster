from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from teachers.models import Teacher
from core.serializers import UserProfileRelationSerializer


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
        read_only_fields = ('token',)

    def validate_user(self, value):
        '''Raise error if user is not a student.'''
        if not value.is_student():
            raise ValidationError('You cannot promote non-student users.')

        return value

    def create(self, validated_data):
        validated_data.setdefault('promoted_by', self.context['request'].user)
        return super().create(validated_data)


class TeacherRetrieveSerializer(serializers.ModelSerializer):
    user = UserProfileRelationSerializer()

    class Meta:
        model = Teacher
        fields = [
            'user',
            'promoted_by',
            'description',
            'promotion_date',
            'contact_links',
        ]


class TeacherUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = [
            'description',
            'contact_links',
        ]


class TeacherListSerializer(serializers.ModelSerializer):
    user = UserProfileRelationSerializer()

    class Meta:
        model = Teacher
        fields = [
            'user',
            'description',
            'token',
        ]
