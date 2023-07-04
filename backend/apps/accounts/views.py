from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import (
    AccountRegisterSerializer,
    AccountVerifySerializer,
    ResendCodeSerializer
)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


@extend_schema_view(
    post=extend_schema(
        description='''Register a new user.''',
        request=AccountRegisterSerializer,
        responses={
            '201': 'ok',
            '202': 'User already exists, but not verified',
            '400': 'An active user already exists',
        },
        tags=['Authentication'],
    ),
)
class UserRegisterView(CreateAPIView):
    serializer_class = AccountRegisterSerializer


@extend_schema_view(
    post=extend_schema(
        description='''Verify deactive account.''',
        request=AccountVerifySerializer,
        responses={
            '200': 'ok',
            '400': 'Invalid data',
            '404': 'User not found',
            '409': 'User is already verified'
        },
        tags=['Authentication'],
    ),
)
class UserVerifyView(APIView):
    serializer_class = AccountVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.verify_code(
                email=serializer.validated_data['email'],
                code=serializer.validated_data['code'],
            )
            return Response("Account verified", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        description='''Resend Verification Code.''',
        request=AccountVerifySerializer,
        responses={
            '201': 'New Verification Code sent to user',
            '400': 'Invalid Data',
            '404': 'User not found',
            '409': 'An active code already sent to user',
        },
        tags=['Authentication'],
    ),
)
class ResendCodeView(CreateAPIView):
    '''Resend a new verification code for the user'''
    serializer_class = ResendCodeSerializer


@extend_schema_view(
    post=extend_schema(
        description='''Get Access/Refresh Token''',
        responses={
            '200': 'Success',
            '400': 'Invalid data',
            '401': 'Unauthorized',
        },
        tags=['Authentication'],
    ),
)
class TokenObtainView(TokenObtainPairView):
    pass
