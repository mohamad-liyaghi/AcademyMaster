from rest_framework import status
from rest_framework.exceptions import APIException


class DuplicateUserException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A user with this email address already exists.'
    default_code = 'user_exists'


class PendingVerificationException(APIException):
    status_code = status.HTTP_202_ACCEPTED
    detail = '''
        An unverified user exists with this email. Please verify your account.
        '''


class AlreadyVerifiedException(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User is already verified.'


class InvalidVerificationCodeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Code is either invalid or expired.'
