from django.urls import path, include
from accounts.views import UserRegisterView

app_name = 'accounts'

v1_urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register')
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
