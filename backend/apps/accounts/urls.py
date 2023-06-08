from django.urls import path, include
from accounts.views import (
    UserRegisterView,
    UserVerifyView,
    TokenObtainView,
)

app_name = 'accounts'

v1_urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify/', UserVerifyView.as_view(), name='verify'),
    path('login/', TokenObtainView.as_view(), name='login'),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
