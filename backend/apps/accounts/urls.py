from django.urls import path, include
from accounts.views import (
    UserRegisterView,
    UserVerifyView,
    ResendCodeView,
    TokenObtainView,
)

app_name = "accounts"

v1_urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("verify/", UserVerifyView.as_view(), name="verify"),
    path("resend/", ResendCodeView.as_view(), name="resend_code"),
    path("login/", TokenObtainView.as_view(), name="login"),
]

urlpatterns = [path("v1/", include(v1_urlpatterns))]
