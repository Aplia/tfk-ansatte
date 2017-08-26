"""backend URL Configuration """
from django.conf import settings
from django.conf.urls import url, include
from backend.api import router


urlpatterns = [
    url(r'^backend/api/', include(router.urls)),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^backend/__debug__/', include(debug_toolbar.urls)),
    ]
