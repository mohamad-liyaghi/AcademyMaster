import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestRetrieveCourseView:

    @pytest.fixture(autouse=True)
    def setup(self, create_course):
        self.url_path = reverse(
            'courses:retrieve_course',
            kwargs={'course_token': create_course.token}
        )

    def test_retrieve_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_authorized(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
