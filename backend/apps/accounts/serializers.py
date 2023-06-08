from rest_framework import serializers
from django.shortcuts import get_object_or_404
from accounts.exceptions import (
    DuplicateUserException,
    PendingVerificationException,
    InvalidVerificationCodeException,
    AlreadyVerifiedException

)
from accounts.models import Account, VerificationCode


class AccountRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = Account
        fields = ["email", "first_name", "last_name", "password"]

    def validate_email(self, value):
        '''
            Ensure user with email does not exist
        '''

        email = value
        account = Account.objects.filter(email=email).first()

        if account:
            if account.is_active:
                raise DuplicateUserException()

            VerificationCode.objects.check_or_create(user=account)
            raise PendingVerificationException()

        return value

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user


class AccountVerifySerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = VerificationCode
        fields = ['email', 'code']

    def verify_code(self, email: str, code: int):
        user = get_object_or_404(Account, email=email)

        if user.is_active:
            raise AlreadyVerifiedException()

        verify_code = VerificationCode.objects.verify(user=user, code=code)

        if not verify_code:
            raise InvalidVerificationCodeException()

        user.is_active = True
        user.save()
        return user
