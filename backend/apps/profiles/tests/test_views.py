from django.urls import reverse
from rest_framework import status
import pytest
from core.tests import user, superuser, api_client
from profiles.models import Profile


@pytest.mark.django_db
class TestUpdateProfileView:

    def setup(self):
        self.data = {
            'birth_date': '1990-01-01',
            'address': 'Fake addr',
            'passport_id': '1234',
            'phone_number': '+989919919911',
        }

    def test_update_profile_unauthorized(self, superuser, api_client):
        url = reverse(
            'profiles:update_profile',
            kwargs={'profile_token': superuser.profile.token}
        )
        response = api_client.put(url, self.data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile(self, superuser, api_client):
        api_client.force_authenticate(user=superuser)
        url = reverse(
            'profiles:update_profile',
            kwargs={'profile_token': superuser.profile.token}
        )
        response = api_client.put(url, self.data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_update_profile_invalid_data(self, superuser, api_client):
        api_client.force_authenticate(user=superuser)
        url = reverse(
            'profiles:update_profile',
            kwargs={'profile_token': superuser.profile.token}
        )
        response = api_client.put(url, {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_others_profile(self, superuser, user, api_client):
        other_profile = Profile.objects.create(user=user)
        api_client.force_authenticate(user=superuser)
        url = reverse(
            'profiles:update_profile',
            kwargs={'profile_token': other_profile.token}
        )
        response = api_client.put(url, {}, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
