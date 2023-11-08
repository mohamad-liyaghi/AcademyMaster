from django.urls import path, include
from enrollments.views import (
    EnrollmentListView,
    EnrollmentCreateView,
    EnrollmentRetrieveView,
    EnrollmentUpdateView,
)

app_name = "enrollments"

v1_urlpatterns = [
    path("", EnrollmentListView.as_view(), name="enrollment_list"),
    path("create/", EnrollmentCreateView.as_view(), name="create_enrollment"),
    path(
        "<str:enrollment_token>/",
        EnrollmentRetrieveView.as_view(),
        name="retrieve_enrollment",
    ),
    path(
        "<str:enrollment_token>/update/",
        EnrollmentUpdateView.as_view(),
        name="update_enrollment",
    ),
]


urlpatterns = [path("v1/", include(v1_urlpatterns))]
