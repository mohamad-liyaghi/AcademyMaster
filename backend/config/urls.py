from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

THIRD_PARTY_URLS = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('download/', SpectacularAPIView.as_view(), name='download-schema'),
    path(
        '',
        SpectacularSwaggerView.as_view(url_name='download-schema'),
        name='swagger-ui'
    ),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    *THIRD_PARTY_URLS,
]
