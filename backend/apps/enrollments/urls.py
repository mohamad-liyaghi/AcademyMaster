from django.urls import path, include
from enrollments.views import (
    EnrollmentCreateView,
    EnrollmentRetrieveView,
)

app_name = 'enrollments'

v1_urlpatterns = [
    path('create/', EnrollmentCreateView.as_view(), name='create_enrollment'),
    path(
        '<str:enrollment_token>/',
        EnrollmentRetrieveView.as_view(),
        name='retrieve_enrollment'
    ),
]


urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
