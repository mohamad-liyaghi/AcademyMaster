from django.urls import path, include
from managers.views import (
    ManagerCreateView,
)

app_name = 'managers'

v1_urlpatterns = [
    path('create/', ManagerCreateView.as_view(), name='create_manager'),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
