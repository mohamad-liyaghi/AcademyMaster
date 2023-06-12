from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as ModelValidationError
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
