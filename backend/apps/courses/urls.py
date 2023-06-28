from django.urls import path, include
from courses.views import (
    CourseCreateView,
    CourseRetrieveView
)

app_name = 'courses'

v1_urlpatterns = [
    path('create/', CourseCreateView.as_view(), name='create_course'),
    path(
        '<str:course_token>/',
        CourseRetrieveView.as_view(),
        name='retrieve_course'
    ),
]


urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
