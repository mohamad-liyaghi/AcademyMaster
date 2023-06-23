import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestVerifyUserView:

    @pytest.fixture(autouse=True)
    def setup(self, deactive_account):
        self.verification_code = deactive_account.verification_codes.first()
        self.data = {
            'email': deactive_account.email,
            'code': self.verification_code.code,
        }
        self.url_path = reverse('accounts:verify')

    def test_verify_user(self, api_client):
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_200_OK

    def test_verify_user_false_code(self, api_client):
        self.data['code'] = self.verification_code.code + str(12)
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verify_active_user(self, api_client, active_account):
        self.data['email'] = active_account.email

        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_verify_invalid_user(self, api_client):
        self.data['email'] = 'not@exist.com'
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_verify_invalid_data(self, api_client):
        response = api_client.post(
            self.url_path, {}, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
