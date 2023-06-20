from django.urls import path, include
from teachers.views import (
    TeacherCreateView,
    TeacherRetrieveView,
    TeacherUpdateView,
)

app_name = 'teachers'

v1_urlpatterns = [
    path('create/', TeacherCreateView.as_view(), name='create_teacher'),
    path(
        '<str:teacher_token>/',
        TeacherRetrieveView.as_view(),
        name='retrieve_teacher'
    ),
    path(
        '<str:teacher_token>/update/',
        TeacherUpdateView.as_view(),
        name='update_teacher'
    ),
]


urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
