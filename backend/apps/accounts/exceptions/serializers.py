from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyExistsException(APIException):
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


class DuplicationCodeException(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'An active verification code for given account already exists.'
