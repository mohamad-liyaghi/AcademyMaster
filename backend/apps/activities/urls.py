from django.urls import path, include
from activities.views import (
    ActivityRetrieveView,
)

app_name = 'activities'

v1_urlpatterns = [
    path(
        '<str:activity_token>/',
        ActivityRetrieveView.as_view(),
        name='retrieve_activity'
    ),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
