# -*- coding: utf-8 -*-
# noinspection PyUnresolvedReferences
from .base import *

# ==============================================================================
# Core
# ==============================================================================

# Debug is on by default for dev, but can be turned off in a .env file
DEBUG = env.bool('DJANGO_DEBUG', True)

SECRET_KEY = env('DJANGO_SECRET_KEY', default='_ln(va4$*2n7cumgmz#3*s123mf&0hx250bf87y!t(h(wvgx')

# Debug toolbar is on by default, can be turned off in a .env file
if env.bool('DJANGO_DEBUG_TOOLBAR', True):
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]

    INSTALLED_APPS += (
        'debug_toolbar',
    )

if env.bool('USE_DOCKER', False):
    # Fix for debug toolbar when running through nginx reverse proxy in docker
    MIDDLEWARE = ['backend.middleware.SetRemoteAddrMiddleware'] + MIDDLEWARE

CORS_ORIGIN_ALLOW_ALL = True
