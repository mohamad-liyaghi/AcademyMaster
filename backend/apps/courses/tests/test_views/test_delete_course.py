import pytest
from django.urls import reverse
from rest_framework import status
from courses.models import Course, CourseStatus


@pytest.mark.django_db
class TestDeleteCourseView:

    @pytest.fixture(autouse=True)
    def setup(self, create_course):
        self.course = create_course
        self.url_path = reverse(
            'courses:delete_course',
            kwargs={'course_token': create_course.token}
        )

    def test_delete_unauthorized(self, api_client):
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Course.objects.count() == 0

    def test_delete_by_accessed_manager(
        self, api_client, accessed_manager_account
    ):
        api_client.force_authenticate(accessed_manager_account)
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Course.objects.count() == 0

    def test_delete_by_manager_no_perm(
        self, api_client, manager_account
    ):
        assert not manager_account.has_perm(
            perm_object=Course.get_permission('delete')
        )
        api_client.force_authenticate(manager_account)
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_completed_course(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        self.course.status = CourseStatus.COMPLETED
        self.course.save()
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_in_progress_without_enrollments(self):
        pass

    def test_delete_in_progress_with_enrollments(self):
        pass


# TODO check enrollments before deleting
