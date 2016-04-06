"""
Django settings for testing
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '1234567890'

DEBUG = True

ALLOWED_HOSTS = []

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',
    'guardian',
    'ninecms',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'tests', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True,
        },
    },
]

# WSGI_APPLICATION = 'ninecms_starter.wsgi.application'

ROOT_URLCONF = 'tests.urls'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}


# Internationalization

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('el', 'Greek'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


# Media

MEDIA_ROOT = os.path.join(BASE_DIR, 'tests', 'media')

MEDIA_URL = '/media/'


# Error reporting

ADMINS = (
    ("Webmaster", "web@9-dev.com"),
)

MANAGERS = (
    ("Webmaster", "web@9-dev.com"),
)

EMAIL_HOST = 'mail.9-dev.com'

EMAIL_HOST_USER = 'do-not-reply@9-dev.com'

EMAIL_HOST_PASSWORD = ''

EMAIL_USE_SSL = True

EMAIL_PORT = 465

EMAIL_SUBJECT_PREFIX = '[9cms] '

SERVER_EMAIL = 'do-not-reply@9-dev.com'

DEFAULT_FROM_EMAIL = 'do-not-reply@9-dev.com'


# Security

LOGIN_URL = '/admin/login/'

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_NAME = 'ninecms_sessionid'


# Caches

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CACHE_MIDDLEWARE_SECONDS = 3 * 60 * 60  # or whatever


# Guardian

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1


# Django admin

DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

# MESSAGE_TAGS = {
#     messages.SUCCESS: 'alert-success success',
#     messages.WARNING: 'alert-warning warning',
#     messages.ERROR: 'alert-danger error'
# }


# NineCMS settings

# noinspection PyUnresolvedReferences
from ninecms.settings import *

IMAGE_STYLES.update({
    'thumbnail-upscale': {
        'type': 'thumbnail-upscale',
        'size': (150, 150)
    },
})
