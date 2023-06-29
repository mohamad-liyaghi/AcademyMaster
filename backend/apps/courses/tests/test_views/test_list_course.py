import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class CourseListViewTest:

    @pytest.fixture(autouse=True)
    def setup(self, create_course):
        self.url_path = reverse(
            'courses:list_courses',
        )

    def test_list_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_authorized(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
