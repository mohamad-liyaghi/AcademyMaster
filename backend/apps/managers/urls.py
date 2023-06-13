from django.urls import path, include

app_name = 'managers'

v1_urlpatterns = []

urlpatterns = [
    path('v1', include(v1_urlpatterns))
]
