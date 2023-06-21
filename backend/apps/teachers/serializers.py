from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from teachers.models import Teacher
from profiles.models import Profile


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


class TeacherProfileSerializer(serializers.ModelSerializer):
    '''The profile of the user'''
    full_name = serializers.SerializerMethodField(method_name='get_full_name')

    class Meta:
        model = Profile
        fields = [
            'full_name',
            'avatar',
            'token'
        ]

    def get_full_name(self, value):
        return value.user.full_name


class TeacherRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_teacher_profile')

    class Meta:
        model = Teacher
        fields = [
            'user',
            'promoted_by',
            'description',
            'promotion_date',
            'contact_links',
        ]

    def get_teacher_profile(self, teacher):
        try:
            profile = teacher.user.profile
            serializer = TeacherProfileSerializer(profile)
            return serializer.data

        except Exception:
            return None


class TeacherUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = [
            'promotion_date',
            'contact_links',
        ]


class TeacherListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Teacher
        fields = [
            'user',
            'description',
            'token',
        ]
