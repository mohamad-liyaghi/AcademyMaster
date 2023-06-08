from django.urls import path, include
from accounts.views import UserRegisterView, UserVerifyView

app_name = 'accounts'

v1_urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify/', UserVerifyView.as_view(), name='verify'),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
