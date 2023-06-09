from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import Account
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestRegisterUserView:

    def setup(self):
        self.data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
        }

    def test_register_valid_user_returns_created(self, api_client):
        response = api_client.post(
            reverse('accounts:register'), self.data, format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_register_duplicated_user(self, api_client, superuser):
        self.data['email'] = superuser.email
        response = api_client.post(
            reverse('accounts:register'), self.data, format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicated_expired_token(self, api_client, user):
        verification = user.verification_codes.first()
        verification.expire_at -= timedelta(days=2)
        verification.save()

        self.data['email'] = user.email
        response = api_client.post(
            reverse('accounts:register'), self.data, format='json'
        )

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert user.verification_codes.count() == 2

    def test_register_duplicated_valid_token(self, api_client, user):
        verification = user.verification_codes.first()
        verification.is_valid = True
        verification.save()

        self.data['email'] = user.email
        response = api_client.post(
            reverse('accounts:register'), self.data, format='json'
        )

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert verification.is_valid == True
        assert user.verification_codes.count() == 1


@pytest.mark.django_db
class TestVerifyUserView:

    def setup(self):
        self.user = Account.objects.create_user(
            email='fake@fake.com', password='1234EErr'
        )
        verification_code = self.user.verification_codes.first().code
        self.data = {
            'email': self.user.email,
            'code': verification_code,
        }

    def test_verify_user(self, api_client):
        response = api_client.post(
            reverse('accounts:verify'), self.data, format='json'
        )
        assert response.status_code == status.HTTP_200_OK

    def test_verify_active_user(self, api_client):
        self.user.is_active = True
        self.user.save()
        response = api_client.post(
            reverse('accounts:verify'), self.data, format='json'
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_verify_invalid_user(self, api_client):
        self.data['email'] = 'not@exist.com'
        response = api_client.post(
            reverse('accounts:verify'), self.data, format='json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_verify_invalid_data(self, api_client):
        response = api_client.post(
            reverse('accounts:verify'), {}, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestObtainTokenView:
    def setup(self):
        password = '1234EErr'
        self.user = Account.objects.create_superuser(
            email='fake@fake.com', password=password
        )
        self.data = {
            'email': self.user.email,
            'password': password
        }

    def test_get_access_token(self, api_client):
        response = api_client.post(
            reverse('accounts:login'), self.data, format='json'
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_access_token_non_existance_user(self, api_client):
        response = api_client.post(
            reverse('accounts:login'), 
            {
                'email': 'non@exist.com', 'password': '1234EErr'
            }, format='json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {
            "detail": "No active account found with the given credentials"
        }

    def test_get_access_token_invalid_data(self, api_client):
        self.data['password'] = 'invalid_password'
        response = api_client.post(
            reverse('accounts:login'), self.data, format='json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
