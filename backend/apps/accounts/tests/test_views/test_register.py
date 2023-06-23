import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import Account


@pytest.mark.django_db
class TestRegisterUserView:

    def setup(self):
        self.data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
        }
        self.url_path = reverse('accounts:register')

    def test_register(self, api_client):
        response = api_client.post(
            self.url_path, self.data, format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Account.objects.count() == 1

    def test_register_duplicate_user(self, api_client, superuser):
        '''Return 400 bad request for email duplication'''
        self.data['email'] = superuser.email
        response = api_client.post(
            self.url_path, self.data, format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Account.objects.count() == 1

    def test_register_active_user_exist(self, api_client, active_account):
        self.data['email'] = active_account.email
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_deactive_user_exists(self, api_client, deactive_account):
        self.data['email'] = deactive_account.email
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
