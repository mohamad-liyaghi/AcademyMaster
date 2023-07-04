import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestRetrieveActivityView:

    @pytest.fixture(autouse=True)
    def setup(self, get_activity):
        self.activity = get_activity
        self.url_path = reverse(
            'activities:retrieve_activity',
            kwargs={'activity_token': get_activity.token}
        )

    def test_retrieve_unauthenticated(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_by_activiy_user(self, api_client):
        api_client.force_authenticate(user=self.activity.user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_admin(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_teacher(self, api_client, teacher_account):
        api_client.force_authenticate(user=teacher_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_manager(self, api_client, manager_account):
        api_client.force_authenticate(user=manager_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_other_student(self, api_client, active_account):
        api_client.force_authenticate(user=active_account)
        assert active_account != self.activity.user
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN
