import pytest
from django.urls import reverse
from rest_framework import status
from teachers.models import Teacher


@pytest.mark.django_db
class TestTeacherCreateView:

    @pytest.fixture(autouse=True)
    def setup(self, active_account):
        self.url_path = reverse('teachers:create_teacher')
        self.user = active_account

        self.data = {
            "user": self.user.token,
        }

    def test_create_unauthorized(self, api_client):
        response = api_client.post(self.url_path, self.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.post(self.url_path, self.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.user.is_teacher()
        assert self.user.teacher.promoted_by == superuser

    def test_create_by_accessed_manager(
            self, api_client, accessed_manager_account
    ):
        api_client.force_authenticate(accessed_manager_account)
        response = api_client.post(self.url_path, self.data)
        assert accessed_manager_account.has_perm(
            perm_object=Teacher.get_permission('add')
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert self.user.is_teacher()
        assert self.user.teacher.promoted_by == accessed_manager_account

    def test_create_by_manager_no_perm(self, api_client, manager_account):
        api_client.force_authenticate(manager_account)
        response = api_client.post(self.url_path, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not manager_account.has_perm(
            perm_object=Teacher.get_permission('add')
        )
        assert not self.user.is_teacher()

    def test_promote_admin(self, api_client, superuser):
        '''Cannot promote admins as teacher'''
        api_client.force_authenticate(superuser)

        assert not superuser.is_student()
        self.data['user'] = superuser.token

        api_client.force_authenticate(superuser)
        response = api_client.post(self.url_path, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_promote_manager(
            self, api_client, manager_account, superuser
    ):
        '''Cannot promote managers as teacher'''
        api_client.force_authenticate(superuser)
        assert not manager_account.is_student()
        self.data['user'] = manager_account.token

        response = api_client.post(self.url_path, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_promote_teacher_twice(
            self, api_client, teacher_account, superuser
    ):
        '''Cannot promote teacher twice'''
        api_client.force_authenticate(superuser)

        self.data['user'] = teacher_account.token

        response = api_client.post(self.url_path, self.data)
        assert not teacher_account.is_student()
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_promote_teacher_bad_data(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.post(self.url_path, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
