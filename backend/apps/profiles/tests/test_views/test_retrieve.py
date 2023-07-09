from django.urls import reverse
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestRetrieveProfileView:

    def setup(self):
        self.url_path = 'profiles:retrieve_profile'

    def test_retrieve_profile_unauthorized(self, superuser, api_client):
        url = reverse(
            self.url_path,
            kwargs={'profile_token': superuser.profile.token}
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_profile(self, superuser, api_client):
        api_client.force_authenticate(user=superuser)
        url = reverse(
            self.url_path,
            kwargs={'profile_token': superuser.profile.token}
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_others_via_student(
            self, superuser, active_account, api_client
    ):
        '''Students cannot get others profile'''
        assert active_account.is_student()
        api_client.force_authenticate(user=active_account)

        url = reverse(
            self.url_path,
            kwargs={'profile_token': superuser.profile.token}
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_student_get_own_profile(self, active_account, api_client):
        '''
        Even though student cannot access others profile page
        But the owned profile is allowed
        '''
        api_client.force_authenticate(user=active_account)
        profile = active_account.profile
        url = reverse(
            self.url_path,
            kwargs={'profile_token': profile.token}
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_non_exist_profile(self, superuser, api_client, unique_uuid):
        api_client.force_authenticate(user=superuser)
        url = reverse(
            self.url_path,
            kwargs={'profile_token': unique_uuid}
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
