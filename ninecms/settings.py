""" Settings default definition for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

""" Default recommended settings """
# INSTALLED_APPS = (
#     'admin_bootstrapped_plus',
#     # 'bootstrap3',
#     'django_admin_bootstrapped',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'mptt',
#     'debug_toolbar',
#     'guardian',
#     'ninecms',
#     'myproject_core'
# )
#
# MIDDLEWARE_CLASSES = (
#     'django.middleware.cache.UpdateCacheMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.locale.LocaleMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.cache.FetchFromCacheMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
# )

# ROOT_URLCONF = 'myproject.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [
#             os.path.join(BASE_DIR,  'templates'),
#         ],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#             'debug': True,
#         },
#     },
# ]

# WSGI_APPLICATION = 'myproject.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# LANGUAGE_CODE = 'el'
#
# LANGUAGES = (
#     ('el', 'Greek'),
#     # ('en', 'English'),
# )
#
# TIME_ZONE = 'Europe/Athens'

# USE_I18N = True
#
# USE_L10N = True
#
# USE_TZ = True

# STATIC_URL = '/static/'
#
# # Following remains for PyCharm code inspections in templates; deprecated in Django 1.8
# TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR,  'templates'),
# )

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
# )

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#
# MEDIA_URL = '/media/'

# LOGIN_URL = '/admin/login/'

# # Error reporting
#
# ADMINS = (
#     ("Webmaster", "web@9-dev.com"),
# )
#
# MANAGERS = (
#     ("Webmaster", "web@9-dev.com"),
# )
#
# EMAIL_HOST = 'mail.9-dev.com'
#
# EMAIL_HOST_USER = 'ninecms@9-dev.com'
#
# EMAIL_HOST_PASSWORD = ''
#
# EMAIL_USE_SSL = True
#
# EMAIL_PORT = 465
#
# EMAIL_SUBJECT_PREFIX = '[9cms] '
#
# SERVER_EMAIL = 'ninecms@9-dev.com'
#
# DEFAULT_FROM_EMAIL = 'ninecms@9-dev.com'
#
#
# # Security
# # http://django-secure.readthedocs.org/en/latest/settings.html
#
# SECURE_CONTENT_TYPE_NOSNIFF = True
#
# SECURE_BROWSER_XSS_FILTER = True
#
# X_FRAME_OPTIONS = 'DENY'
#
# CSRF_COOKIE_HTTPONLY = True
#
# # SSL only
# # SECURE_SSL_REDIRECT = True
#
# # SECURE_HSTS_SECONDS = 31536000
#
# # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#
# # SESSION_COOKIE_SECURE = True
#
# # CSRF_COOKIE_SECURE = True

# # Add unique session cookie name for concurrent logins with other sites
# SESSION_COOKIE_NAME = 'myapp_sessionid'
#
# # Caches
# # https://docs.djangoproject.com/en/1.8/topics/cache/
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }
#
# CACHE_MIDDLEWARE_SECONDS = 3 * 60 * 60

# # Guardian
# # https://django-guardian.readthedocs.org/en/v1.2/configuration.html
#
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',  # this is default
#     'guardian.backends.ObjectPermissionBackend',
# )
#
# ANONYMOUS_USER_ID = -1

# # Django admin
# DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'
#
# MESSAGE_TAGS = {
#     messages.SUCCESS: 'alert-success success',
#     messages.WARNING: 'alert-warning warning',
#     messages.ERROR: 'alert-danger error'
# }


""" Test """
# from myapp.settings import *
#
# DEBUG = True
#
# PASSWORD_HASHERS = (
#     'django.contrib.auth.hashers.MD5PasswordHasher',
# )
#
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [  # disable overriden templates
#         ],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#             'debug': True,
#         },
#     },
# ]
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
#
# LANGUAGES = (
#     ('el', 'Greek'),
#     ('en', 'English'),
# )
#
# IMAGE_STYLES.update({
#     'thumbnail-upscale': {
#         'type': 'thumbnail-upscale',
#         'size': (150, 150)
#     },
# })

""" Live """
# # noinspection PyUnresolvedReferences
# from myapp.settings import *
#
# DEBUG = False
#
# ALLOWED_HOSTS = [
#     '',
# ]
#
# TEMPLATE_DIRS = None
#
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [
#             os.path.join(BASE_DIR,  'templates'),
#         ],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]
#
# STATIC_ROOT = '/var/www'
#
# STATICFILES_DIRS = []
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#         'TIMEOUT': 3 * 60 * 60,  # 3h
#         'KEY_PREFIX': 'rabelvideo_',
#         'VERSION': 1,
#     }
# }


""" CMS """

# Site name to display in title etc.
SITE_NAME = "9cms"

# Meta author tag
SITE_AUTHOR = "9cms"

# Meta keywords
SITE_KEYWORDS = ""

# Define image styles
IMAGE_STYLES = {
    'thumbnail': {
        'type': 'thumbnail',
        'size': (150, 1000)
    },
    'thumbnail_crop': {
        'type': 'thumbnail-crop',
        'size': (150, 150)
    },
    'thumbnail_upscale': {
        'type': 'thumbnail-upscale',
        'size': (150, 150)
    },
    'gallery_style': {
        'type': 'thumbnail',
        'size': (400, 1000)
    },
    'blog_style': {
        'type': 'thumbnail-crop',
        'size': (350, 226)
    },
    'large': {
        'type': 'thumbnail',
        'size': (1280, 1280)
    },
}

# Update image styles in project settings such as:
# IMAGE_STYLES.update({})

# Define characters to remove at transliteration
TRANSLITERATE_REMOVE = '"\'`,:;|{[}]+=*&%^$#@!~()?<>'

# Define characters to replace at transliteration
TRANSLITERATE_REPLACE = (' .-_/', '-----')

# Define language menu labels
# Possible values: name, code, flag
LANGUAGE_MENU_LABELS = 'name'

# Enable i18n urls for 9cms
I18N_URLS = True
