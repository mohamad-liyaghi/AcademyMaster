from django.urls import path, include
from activities.views import (
    CourseActivityListView,
    ActivityRetrieveView,
    ActivityUpdateView,
)

app_name = "activities"

v1_urlpatterns = [
    path("<str:course_token>/", CourseActivityListView.as_view(), name="activity_list"),
    path(
        "<str:course_token>/<str:activity_token>/",
        ActivityRetrieveView.as_view(),
        name="retrieve_activity",
    ),
    path(
        "<str:course_token>/<str:activity_token>/update/",
        ActivityUpdateView.as_view(),
        name="update_activity",
    ),
]

urlpatterns = [path("v1/", include(v1_urlpatterns))]
