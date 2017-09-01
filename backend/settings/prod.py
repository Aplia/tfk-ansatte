# -*- coding: utf-8 -*-
# noinspection PyUnresolvedReferences
from .base import *

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': [],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', ],
            'propagate': True
        },
    }
}

# SENTRY ERROR LOGGING
# ------------------------------------------------------------------------------

# Skip sentry if we are deploying
if not DEPLOY_ENV and DJANGO_SENTRY_DSN:
    SENTRY_LOGGING = {
        'filters': {
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
                'class': 'raven.contrib.django.handlers.SentryHandler',
            },
        },
        'loggers': {
        },
    }

    sentry_handlers = SENTRY_LOGGING.get('handlers', {})
    if sentry_handlers:
        LOGGING['handlers'] = dict(LOGGING.get('handlers', {}), **sentry_handlers)
    sentry_loggers = SENTRY_LOGGING.get('loggers', {})
    if sentry_loggers:
        LOGGING['loggers'] = dict(LOGGING.get('loggers', {}), **sentry_loggers)
    sentry_filters = SENTRY_LOGGING.get('filters', {})
    if sentry_filters:
        LOGGING['filters'] = dict(LOGGING.get('filters', {}), **sentry_filters)

    # Add sentry to disallowed host errors
    LOGGING['loggers']['django.security.DisallowedHost']['handlers'].append('sentry')

    RAVEN_CONFIG = {
        'dsn': DJANGO_SENTRY_DSN,
    }

    # Add raven to the list of installed apps
    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]
