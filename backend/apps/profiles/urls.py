from django.urls import path, include
from .views import (
    ProfileUpdateView,
)

app_name = 'profiles'

v1_urlpatterns = [
    path(
        '<str:profile_token>/',
        ProfileUpdateView.as_view(),
        name='update_profile'
    )
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
