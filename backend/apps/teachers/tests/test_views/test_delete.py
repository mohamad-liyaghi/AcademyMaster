import pytest
from django.urls import reverse
from rest_framework import status
from managers.models import Manager


@pytest.mark.django_db
class TestTeacherDeleteView:

    @pytest.fixture(autouse=True)
    def setup(self, teacher_account):
        self.teacher = teacher_account
        self.url_name = 'teachers:delete_teacher'
        self.url_path = reverse(
                    self.url_name,
                    kwargs={'teacher_token': self.teacher.teacher.token}
                )

    def test_delete_unauthorized(self, api_client):
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        self.teacher.refresh_from_db()
        assert not self.teacher.is_teacher()

    def test_delete_by_accessed_manager(
            self, api_client, accessed_manager_account
    ):
        api_client.force_authenticate(accessed_manager_account)
        response = api_client.delete(self.url_path)
        assert accessed_manager_account.has_perm(
            perm_object=Manager.get_permission('delete')
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        self.teacher.refresh_from_db()
        assert not self.teacher.is_teacher()

    def test_delete_by_manager_no_permissin(self, api_client, manager_account):
        api_client.force_authenticate(manager_account)
        assert not manager_account.has_perm(
            perm_object=Manager.get_permission('delete')
        )
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_invalid_teacher(self, api_client, superuser, unique_uuid):
        api_client.force_authenticate(superuser)
        response = api_client.delete(
                reverse(
                    self.url_name,
                    kwargs={'teacher_token': unique_uuid}
                ),
            )
        assert response.status_code == status.HTTP_404_NOT_FOUND
