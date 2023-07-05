import pytest
from django.urls import reverse
from rest_framework import status
from courses.models import CourseStatus


@pytest.mark.django_db
class TestUpdateActivityView:

    @pytest.fixture(autouse=True)
    def setup(self, get_activity):
        self.activity = get_activity
        self.url_name = 'activities:update_activity'
        self.url_path = reverse(
            self.url_name,
            kwargs={
                'activity_token': get_activity.token,
                'course_token': get_activity.course.token
            }
        )
        self.data = {
            'attendance': {'session 1': True, 'session 2': False},
        }

    def test_update_unauthenticated(self, api_client):
        response = api_client.patch(self.url_path, self.data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_by_course_instructor(self, api_client):
        api_client.force_authenticate(self.activity.course.instructor.user)
        response = api_client.patch(self.url_path, self.data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_update_by_admin(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.patch(self.url_path, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_by_manager(self, api_client, manager_account):
        api_client.force_authenticate(user=manager_account)
        response = api_client.patch(self.url_path, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_by_student(self, api_client, active_account):
        api_client.force_authenticate(user=active_account)
        response = api_client.patch(self.url_path, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_mark_course_in_perogress(self, api_client):
        api_client.force_authenticate(self.activity.course.instructor.user)
        self.data['final_mark'] = 50
        response = api_client.patch(self.url_path, self.data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_mark_course_completed(self, api_client):
        api_client.force_authenticate(self.activity.course.instructor.user)
        self.activity.course.status = CourseStatus.COMPLETED
        self.activity.course.save()
        self.data['final_mark'] = 50
        response = api_client.patch(self.url_path, self.data, format='json')
        self.activity.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert self.activity.final_mark == 50

    def test_update_not_found(self, api_client):
        api_client.force_authenticate(self.activity.course.instructor.user)
        url_path = reverse(
            self.url_name,
            kwargs={
                'activity_token': 'invalid_token',
                'course_token': 'invalid_course_token'
            }
        )
        response = api_client.patch(url_path, self.data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
