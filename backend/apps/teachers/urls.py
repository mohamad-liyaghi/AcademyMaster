from django.urls import path, include
from teachers.views import (
    ManagerCreateView,
)

app_name = 'teachers'

v1_urlpatterns = [
    path('create/', ManagerCreateView.as_view(), name='create_teacher'),
]


urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
