from django.urls import path, include

app_name = 'accounts'

v1_urlpatterns = []

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
