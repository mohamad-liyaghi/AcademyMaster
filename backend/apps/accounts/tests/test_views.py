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

    def test_register_duplicated_user(self, api_client):
        user = Account.objects.create_superuser(
            email='fake@fake.com', password='1234EErr'
        )

        self.data['email'] = user.email
        response = api_client.post(
            reverse('accounts:register'), self.data, format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicated_expired_token(self, api_client):
        user = Account.objects.create_user(
            email='fake@fake.com', password='1234EErr'
        )
        verification = user.verification_codes.first()
        verification.expire_at -= timedelta(days=2)
        verification.save()

        self.data['email'] = user.email
        response = api_client.post(
            reverse('accounts:register'), self.data, format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert user.verification_codes.count() == 2

    def test_register_duplicated_valid_token(self, api_client):
        user = Account.objects.create_user(
            email='fake@fake.com', password='1234EErr'
        )
        verification = user.verification_codes.first()
        verification.is_valid = True
        verification.save()

        self.data['email'] = user.email
        response = api_client.post(
            reverse('accounts:register'), self.data, format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert verification.is_valid
        assert user.verification_codes.count() == 1
