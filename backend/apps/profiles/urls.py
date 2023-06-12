from django.urls import path, include
from .views import (
    ProfileUpdateView,
    ProfileRetrieveView,
)

app_name = 'profiles'

v1_urlpatterns = [
    path(
        '<str:profile_token>/',
        ProfileRetrieveView.as_view(),
        name='retrieve_profile'
    ),
    path(
        '<str:profile_token>/update/',
        ProfileUpdateView.as_view(),
        name='update_profile'
    ),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
