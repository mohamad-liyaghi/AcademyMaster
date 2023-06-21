from django.urls import reverse
from rest_framework import status
import pytest
from core.tests import user, teacher, superuser, api_client, manager
from teachers.models import Teacher
from managers.models import Manager
from accounts.models import Account


@pytest.mark.django_db
class TestTeacherCreateView:

    def setup(self):
        self.create_url = reverse('teachers:create_teacher')
        self.user = Account.objects.create_user(
            email='teacher@email.com', password='1234EErr'
        )
        self.data = {
            "user": self.user.token,
        }

    def test_unauthorized(self, api_client):
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_teacher(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.user.teacher.promoted_by == superuser

    def test_create_teacher_by_manager_permission_denied(self, api_client, manager):
        assert not manager.has_perm(perm_object=Teacher.get_permission('add'))
        api_client.force_authenticate(manager)
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_promote_non_student(self, api_client, manager, superuser):
        assert not manager.is_student()
        self.data['user'] = manager.token

        api_client.force_authenticate(superuser)
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_duplication_promote(self, api_client, superuser, teacher):
        assert not teacher.is_student()
        self.data['user'] = teacher.token
        api_client.force_authenticate(superuser)
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestTeacherRetrieveView:

    def test_retrieve_unauthorized(self, api_client, teacher):
        resp = api_client.get(
                reverse(
                    'teachers:retrieve_teacher', 
                    kwargs={'teacher_token': teacher.teacher.token}
                )
            )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_teacher(self, api_client, teacher, user):
        api_client.force_authenticate(user)
        resp = api_client.get(
                reverse(
                    'teachers:retrieve_teacher', 
                    kwargs={'teacher_token': teacher.teacher.token}
                )
            )
        assert resp.status_code == status.HTTP_200_OK

    def test_retrieve_not_found(self, api_client, teacher, user):
            api_client.force_authenticate(user)
            resp = api_client.get(
                reverse(
                    'teachers:retrieve_teacher',
                    kwargs={'teacher_token': 'Invalid'}
                )
            )
            assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTeacherUpdateView:
    def test_unauthorized(self, api_client, teacher):
        resp = api_client.put(
                reverse(
                    'teachers:update_teacher', 
                    kwargs={'teacher_token': teacher.teacher.token}
                ),
                {}
            )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update(self, api_client, teacher):
        api_client.force_authenticate(teacher)
        resp = api_client.put(
                reverse(
                    'teachers:update_teacher', 
                    kwargs={'teacher_token': teacher.teacher.token}
                ),
                {
                    'description': 'Updated description'
                }
            )
        assert resp.status_code == status.HTTP_200_OK

    def test_update_others(self, api_client, teacher, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.put(
                reverse(
                    'teachers:update_teacher', 
                    kwargs={'teacher_token': teacher.teacher.token}
                ),
                {
                    'description': 'Updated description'
                }
            )
        assert resp.status_code == status.HTTP_403_FORBIDDEN


    def test_update_no_found(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.put(
                reverse(
                    'teachers:update_teacher', 
                    kwargs={'teacher_token': 'fake_token'}
                ),
            )
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTeacherDeleteView:
    def test_unauthorized(self, api_client, teacher):
        resp = api_client.delete(
                reverse(
                    'teachers:delete_teacher',
                    kwargs={'teacher_token': teacher.teacher.token}
                ),
            )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete(self, api_client, teacher, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.delete(
                reverse(
                    'teachers:delete_teacher',
                    kwargs={'teacher_token': teacher.teacher.token}
                ),
            )
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_no_permission(self, api_client, teacher, manager):
        api_client.force_authenticate(manager)
        assert not manager.has_perm(
            perm_object=Manager.get_permission('delete')
        )
        resp = api_client.delete(
                reverse(
                    'teachers:delete_teacher',
                    kwargs={'teacher_token': teacher.teacher.token}
                ),
            )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_not_found(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.delete(
                reverse(
                    'teachers:delete_teacher',
                    kwargs={'teacher_token': 'invalid_token'}
                ),
            )
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTeacherListView:
    def test_unauthorized(self, api_client, teacher):
        resp = api_client.get(
                reverse(
                    'teachers:teacher_list',
                ),
            )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_list(self, api_client, user):
        api_client.force_authenticate(user)
        resp = api_client.get(
                reverse(
                    'teachers:teacher_list',
                ),
            )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()['count'] == 0

    def test_get_list_with_teahcer(self, api_client, user, teacher):
        api_client.force_authenticate(user)
        resp = api_client.get(
                reverse(
                    'teachers:teacher_list',
                ),
            )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()['count'] == 1
