from django.urls import path, include
from enrollments.views import (
    EnrollmentCreateView,
)

app_name = 'enrollments'

v1_urlpatterns = [
    path('create/', EnrollmentCreateView.as_view(), name='create_enrollment'),
]


urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
