from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as ModelValidationError
from django.contrib.auth import get_user_model
from profiles.models import Profile


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'avatar',
            'birth_date',
            'address',
            'passport_id',
            'phone_number',
        ]

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)

        except ModelValidationError as message:
            raise ValidationError(
                detail=str(*message)
            )


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name'
        ]


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    user = ProfileUserSerializer()

    class Meta:
        model = Profile
        fields = [
            'user',
            'avatar',
            'birth_date',
            'address',
            'passport_id',
            'phone_number',
            'age',
        ]
