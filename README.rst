=======
NineCMS
=======

Nine CMS is a simple Django app to manage content. Users can create content and publish it to various paths.

Detailed documentation soon to be published.

Screenshots under the ``docs/`` project directory.

.. image:: https://raw.githubusercontent.com/Wtower/django-ninecms/master/docs/screenshots/index1.png

Objectives
----------

It is the author's opinion that heavyweight content management systems are not so important to Django,
as much as established CMS are important to other languages such as PHP.
Django can be very easily used to build exotic web applications in very short time,
therefore too often Django does not need another heavyweight CMS.
Nine CMS is intended to provide a common denominator for simple content when building a Django app or for small sites.

To sum up:

- Lightweight
- Easy to start up AND customize a project
- Inspired by Drupal node model architecture
- Obviously uses the Django web framework on Python

Features
--------

- Node modeling inspired by Drupal nodes featuring:

  - Dynamic content (obviously) rendered as nodes
  - Revisioning system
  - Internationalisation (i18n) right from the beginning
  - URL aliases that may be automatically generated based on provided patterns
  - Page types that may be used in different templates or views (below)
  - Per page type permissions
  - Sanitize HTML

- Content blocks
- Menus
- Media management

  - Images, videos, files
  - Image styles

- Views (requires decoupled signals providing context)
- Taxonomy (terms)
- Contact form
- Admin interface with dashboard
- Utilities

  - Libraries
  - Character transliteration
  - Serializers
  - Custom tags
  - Basic search functionality
  - Template suggestions

- Bootstrap

Dependencies
------------

It is intented to keep the number of external dependencies as low as possible, if no significant reason is necessary. The following are needed:

- Python (3.4+)
- Django (1.8+): Web framework
- django-guardian (1.3+): provide per-page-type permissions
- django-mptt (0.7+): provide trees for tags and menus
- bleach (1.4+): bleach-sanitize user HTML
- Pillow (3+): create different sizes for user images
- pytz (2015+): handle user time zones

The following packages are optional/recommended:

- django-admin-bootstrapped (2.5+): provide a nicer admin interface experience
- django-admin-bootstrapped-plus: improve the admin interface to use in 9cms
- django-bootstrap3: improve the admin fields
- django-debug-toolbar: for obvious reasons
- mysqlclient: or any other db connector
- newrelic: or any other monitoring tool
- python3-memcached: for memory caching

New project guide
-----------------

This is a full guide to create a new project. *Soon a Quick Guide will be added*.

1. Create a new project

  Create a new project, if not existing, and optionally (as a reminder):

  - Create new virtualenv
  - Initialize git and initial commit

2. Dependencies:

  - Add the following to the ``requirements.txt`` file::

    bleach==1.4.2
    Django==1.8.6
    django-guardian==1.3.2
    django-mptt==0.7.4
    django-ninecms==0.5.1
    Pillow==3.0.0
    pytz==2015.7

  - And optionally::

    coverage==4.0.2
    django-admin-bootstrapped==2.5.6
    django-admin-bootstrapped-plus==0.1.1
    django-bootstrap3==6.2.2
    django-debug-toolbar==1.4.0
    mysqlclient==1.3.7
    newrelic==2.58.0.43
    python3-memcached==1.51
    sqlparse==0.1.18

  - Then run::

    $ pip install -r requirements.txt

3. Settings

  All relevant settings sample also exist in ninecms/settings.py as comment.
  From the code samples below remove any settings refer to optional packages that are not installed as above.

  - ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        'admin_bootstrapped_plus',
        'django_admin_bootstrapped',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'mptt',
        'debug_toolbar',
        'guardian',
        'ninecms',
        # ...
    )

  - Middleware::

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

  - Templates

  Add ``'debug': True`` only if planning to have a separate live settings file for your project::

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR,  'templates'),
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

  - Languages::

    LANGUAGE_CODE = 'en'  # or whatever
    LANGUAGES = (
        ('en', 'English'),
        # ('el', 'Greek'),
        # ...
    )
    TIME_ZONE = 'Europe/Athens'  # or whatever
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

  - Media::

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

  - Error reporting::

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

  - Security:

  Replace ``myapp``::

    LOGIN_URL = '/admin/login/'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_NAME = 'myapp_sessionid'

  - Caches::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
    CACHE_MIDDLEWARE_SECONDS = 3 * 60 * 60  # or whatever

  - Guardian::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',  # this is default
        'guardian.backends.ObjectPermissionBackend',
    )
    ANONYMOUS_USER_ID = -1

  - Django admin::

    DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'
    MESSAGE_TAGS = {
        messages.SUCCESS: 'alert-success success',
        messages.WARNING: 'alert-warning warning',
        messages.ERROR: 'alert-danger error'
    }

  - CMS settings::

    from ninecms.settings import *
    SITE_NAME = "..."
    SITE_AUTHOR = "..."
    SITE_KEYWORDS = "..."
    I18N_URLS = True  # False

  - Optional settings for testing (separate file eg ``settings_test.py``)::

    from myapp.settings import *
    DEBUG = True
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [  # disable overriden templates
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
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    LANGUAGES = (  # at least 2
        ('el', 'Greek'),
        ('en', 'English'),
    )
    IMAGE_STYLES.update({
        'thumbnail-upscale': {
            'type': 'thumbnail-upscale',
            'size': (150, 150)
        },
    })

  - Optional settings for live (separate file eg ``settings_live.py``)::

    from myapp.settings import *
    DEBUG = False
    ALLOWED_HOSTS = [
        # ...
    ]
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR,  'templates'),
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
    STATIC_ROOT =  # ...
    STATICFILES_DIRS = []
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': # ...
            'KEY_PREFIX': # ...
            'VERSION': 1,
        }
    }

4. Create empty folders in project root:

  - ``/static/``
  - ``/media/``

    - Optionally copy folder ``ninecms/basic/image/`` to ``/media/ninecms/basic/image`` if you intend to run ninecms tests

5. Run ``./manage.py migrate`` to create the models.

6. Url configuration

  - Include the URL configurations for admin, i18n and 9cms
  - Make sure 9cms URL conf is the last line so the dynamic router catches all URLs.
  - Include ``robots.txt``
  - Include static files for local server

  URL Example::

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^i18n/', include('django.conf.urls.i18n')),
        url(r'^robots\.txt/$', TemplateView.as_view(template_name='ninecms/robots.txt', content_type='text/plain')),
    ]

    # static files (images, css, javascript, etc.)
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # pragma: no cover

    # Last: all remaining pass to CMS
    if settings.I18N_URLS:  # pragma: nocover
        urlpatterns += i18n_patterns(
            url(r'^', include('ninecms.urls', namespace='ninecms')),
        )
    else:  # pragma: nocover
        urlpatterns += [
            url(r'^', include('ninecms.urls', namespace='ninecms')),
        ]

7. Start the development server and visit http://127.0.0.1:8000/admin/ (you'll need the Admin app enabled).

8. Visit http://127.0.0.1:8000/ to view content.

From here on common tasks include:

- Override templates such as:

  - ``index.html``
  - ``site-name.html``
  - ``block_content.html`` and ``block_static.html`` (optionally, to fine tune the fields present and therefore to reduce
    the number of queries executed)

- Add page types
- Add content
- Add menus
- Add blocks

Views
-----

Add a new Django app in your project with ``signals.py`` to listen to the corresponding signal that is declared with
a new content block in admin.
Look at the ``ninecms/signals.py`` file on how to code the signals.

Theme suggestions
-----------------
Add a file in the project's ``templates`` folder, with the following names, in order to override a 9cms template.

- content: ``[block_content]_[page_type]_[node_id]`` (eg ``block_content_basic_5.html``)
- static node: ``[block_static]_[region]_[alias]`` (eg ``block_static_header_blog_1.html``)
- menu: ``[block_menu]_[region]_[menu.id]`` (eg ``block_menu_header_1.html``)
- signal (view): ``[block_signal]_[region]_[signal]`` (eg ``block_signal_header_random_video_node.html``)
- contact form: ``[block_contact]_[region]``
- language menu: ``[block_language]_[region]``

Any combination of ``[]`` is allowed, eg. ``block_content_basic.html`` or ``block_content_5.html``.
Always append ``.html`` extension.

Permissions summary
-------------------

This is a summary of all applicable permissions:

- Django admin:

  - User: is staff (access to admin)
  - User: is superuser (with caution)

    - unconditional access everywhere
    - additional fields for nodes
    - dashboard
    - utilities on dashboard

  - User: add, change, delete
  - Group: add, change, delete
  - Permission: add, change, delete

- Guardian:

  - User-object permissions: add, change, delete
  - Group-object permissions: add, change, delete

- 9cms:

  - Per model permissions: add, change, delete
  - Node: can use full HTML
  - Node: view unpublished
  - Per content type group permissions (provided from Guardian, accessible through 'page types' change-list admin page)

Example of configuration of an ``editor`` group perms:

- Node: view unpublished
- Node: add
- Node: change
- Image: add, change, delete
- Page type specific permissions: add, change

Important points
----------------

- If i18n urls: menu items for internal pages should always have language [v0.3.1a]
- Theme suggestions [v0.4.4b]
- Search page requires a search results block in page type and 'search' alias, requires MySQL [v0.4.4b]
- When serializing related field using ``table__field`` notation, always add ``select_related`` to query prior calling
  serialize [v0.4.7b]
- Add LANGUAGES in settings_test when I18N_URLS (see aluminium( [v0.4.7b]

Footnote
--------

Any contribution to the project is highly appreciated and the best will be done to respond to it.
