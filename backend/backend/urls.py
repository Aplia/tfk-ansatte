"""backend URL Configuration """
from django.conf import settings
from django.conf.urls import url, include
from backend.api import router
from django.contrib import admin

urlpatterns = [
    url(r'^backend/api/', include(router.urls)),
    url(r'^backend/admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^backend/__debug__/', include(debug_toolbar.urls)),
    ]
