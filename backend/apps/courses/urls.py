from django.urls import path, include
from courses.views import (
    TeacherCreateView,
)

app_name = 'courses'

v1_urlpatterns = [
    path('create/', TeacherCreateView.as_view(), name='create_course')
]


urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
