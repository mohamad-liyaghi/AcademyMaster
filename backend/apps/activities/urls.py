from django.urls import path, include
from activities.views import (
    ActivityRetrieveView,
    ActivityUpdateView,
)

app_name = 'activities'

v1_urlpatterns = [
    path(
        '<str:activity_token>/',
        ActivityRetrieveView.as_view(),
        name='retrieve_activity'
    ),
    path(
        '<str:activity_token>/update/',
        ActivityUpdateView.as_view(),
        name='update_activity'
    ),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
