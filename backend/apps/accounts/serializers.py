from rest_framework import serializers
from accounts.models import VerificationCode, Account


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
                raise serializers.ValidationError(
                    f"An active account with email {email} already exists"
                )

            verification_code = account.verification_codes.first()

            if verification_code and verification_code.is_valid():
                raise serializers.ValidationError(
                    "User already exists, Verify your email."
                )

            else:
                # TODO: Add re-gen verification code
                VerificationCode.objects.create(account=account)
                raise serializers.ValidationError(
                    f"A new verification code has been sent to {email}"
                )

        return value

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user
