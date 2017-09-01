import os

import environ

# Reads environment variables including .env file
env = environ.Env()
env.read_env()

# This is set by deploy scripts when deploying, and contains the type
# of deployment, this is either "production" or "staging"
# This slighly alter configurations to allow the deployment process to work properly.
DEPLOY_ENV = env('DEPLOY_ENV', default=None)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_ln(va4$*2n7cumgmz#3*s123mf&0hx250bf87y!t(h(wvgx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = (
    '0.0.0.0', '127.0.0.1', 'localhost', 'backend', 'tfk-ansatte.aplia.no',
)

INTERNAL_IPS = (
    '0.0.0.0', '127.0.0.1', 'localhost', 'backend', 'tfk-ansatte.aplia.no',
)

if env.bool('USE_DOCKER', False):
    import socket
    # Pass the backend docker ip, reverse proxy ip and the main docker network ip as internal ip and allowed hosts
    # This allows debug toolbar when developing with docker
    backend_ip = socket.gethostbyname(socket.gethostname())
    network_ip = '.'.join(backend_ip.split('.')[:-1] + ['1'])
    ALLOWED_HOSTS += (backend_ip, network_ip, )
    INTERNAL_IPS += (backend_ip, network_ip, )

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'backend',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # needs to be high up/first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

WSGI_APPLICATION = 'backend.wsgi.application'

# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'nb-no'
TIME_ZONE = 'Europe/Oslo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==============================================================================
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
# ==============================================================================

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = '/backend/static/'


# ==============================================================================
# Database
# ==============================================================================

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://postgres:postgres@db/tfk'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# ==============================================================================
# CORS
# ==============================================================================

CORS_ALLOW_CREDENTIALS = True


# SENTRY ERROR LOGGING
# ------------------------------------------------------------------------------
DJANGO_SENTRY_DSN = env(
    "DJANGO_SENTRY_DSN",
    default='')
