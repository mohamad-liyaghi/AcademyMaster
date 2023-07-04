import pytest
from datetime import timedelta
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCodeResendView:
    def setup(self):
        self.url_path = reverse('accounts:resend_code')

    def test_resend_verification_code(self, deactive_account, api_client):
        verification = deactive_account.verification_codes.first()
        verification.expire_at -= timedelta(days=2)
        verification.save()

        assert verification.is_expired()

        response = api_client.post(
            self.url_path,
            {'user': deactive_account.token}, format='json'
        )
        print(response.json())
        assert response.status_code == status.HTTP_201_CREATED
        assert deactive_account.verification_codes.count() == 2

    def test_resend_valid_code_exist(self, deactive_account, api_client):
        '''Do not resend when an active code already exists'''
        verification = deactive_account.verification_codes.first()
        assert not verification.is_expired()

        response = api_client.post(
            self.url_path,
            {'user': deactive_account.token}, format='json'
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert deactive_account.verification_codes.count() == 1

    def test_resend_for_active_user(self, active_account, api_client):
        assert active_account.is_active

        response = api_client.post(
            self.url_path,
            {'user': active_account.token}, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_resend_invalid_data(self, api_client):
        response = api_client.post(self.url_path)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
