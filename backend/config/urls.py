from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

LOCAL_APP_URLS = [
    path('accounts/', include('apps.accounts.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path('managers/', include('apps.managers.urls')),
    path('teachers/', include('apps.teachers.urls')),
    path('courses/', include('apps.courses.urls')),
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

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
        )

handler404 = 'apps.core.views.handler_404'
handler500 = 'apps.core.views.handler_500'
