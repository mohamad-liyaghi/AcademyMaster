from django.urls import path, include
from managers.views import (
    ManagerCreateView,
    ManagerUpdateView,
    ManagerDeleteView,
    ManagerRetrieveView,
)

app_name = 'managers'

v1_urlpatterns = [
    path('create/', ManagerCreateView.as_view(), name='create_manager'),
    path(
        '<str:manager_token>/',
        ManagerRetrieveView.as_view(),
        name='retrieve_manager'
    ),
    path(
        '<str:manager_token>/update/',
        ManagerUpdateView.as_view(),
        name='update_manager'
    ),
    path(
        '<str:manager_token>/delete/',
        ManagerDeleteView.as_view(),
        name='delete_manager'
    ),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
