import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestObtainTokenView:
    @pytest.fixture(autouse=True)
    def setup(self, superuser):
        password = '1234EErr'
        superuser.set_password(password)
        superuser.save()
        self.data = {
            'email': superuser.email,
            'password': password
        }
        self.url_path = reverse('accounts:login')

    def test_get_access_token(self, api_client):
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_access_token_non_existance_user(self, api_client):
        response = api_client.post(
            self.url_path,
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
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_access_token_inactive_user(
            self, deactive_account, api_client
    ):
        self.data['email'] = deactive_account.email
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
