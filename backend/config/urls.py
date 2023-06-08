from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

LOCAL_APP_URLS = [
    path('accounts/', include('apps.accounts.urls'))
]

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
    *LOCAL_APP_URLS,
    *THIRD_PARTY_URLS,
]

handler404 = 'apps.core.views.handler_404'
handler500 = 'apps.core.views.handler_500'
