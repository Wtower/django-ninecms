=======
NineCMS
=======

Nine CMS is a Django app to manage content. Users can create content and publish it to paths.

.. image:: https://img.shields.io/travis/Wtower/django-ninecms/devel.svg
    :target: https://travis-ci.org/Wtower/django-ninecms

.. image:: https://img.shields.io/coveralls/Wtower/django-ninecms/devel.svg
  :target: https://coveralls.io/github/Wtower/django-ninecms

.. image:: https://img.shields.io/pypi/v/django-ninecms.svg
    :target: https://pypi.python.org/pypi/django-ninecms
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/django-ninecms.svg
    :target: https://pypi.python.org/pypi/django-ninecms
    :alt: Number of PyPI downloads per month

Admin screenshot:

.. image:: https://raw.githubusercontent.com/Wtower/django-ninecms/master/docs/screenshots/index1.png

Detailed documentation soon to be published.

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
- Quality: hate bugs; also test coverage is 100%

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

  - Character transliteration
  - Custom tags
  - Basic search functionality

- Bootstrap

Dependencies
------------

The following are needed:

- Python (3.4+)
- Django (1.7+, 1.9 recommended): Web framework
- django-guardian (1.4+): provide per-page-type permissions
- django-mptt (0.8+): provide trees for tags and menus
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

Django 1.9 notices:

- Getting ``RemovedInDjango110Warning: render() must be called with a dict, not a Context.`` to a couple of places.
  Many other apps get similar warnings. Looking for solution without offending Django <1.9.

New project guide
-----------------

This is a full guide to create a new project. *Soon a Quick Guide will be added*.

There is also a project that can be used as an
`Django 9cms web site boilerplate <http://www.github.com/Wtower/django-ninecms-starter>`_.

1. Create a new project

   Create a new project, if not existing, and optionally (as a reminder):

   - Create new virtualenv
   - Initialize git and initial commit

2. Dependencies

   - Add the following to the ``requirements.txt`` file::

       Django~=1.9.0
       django-ninecms>=0.5.4

   - And optionally::

       coverage~=4.0.3
       django-admin-bootstrapped~=2.5.6
       django-admin-bootstrapped-plus>=0.1.1
       django-bootstrap3~=7.0.1
       django-debug-toolbar~=1.4.0
       mysqlclient~=1.3.7
       newrelic~=2.60.0.46
       python3-memcached~=1.51
       sqlparse~=0.1.18

   - Then run::

       $ pip install -r requirements.txt

   - Download CKEditor (optionally) for rich text fields in admin:

     - Download from http://ckeditor.com/builder
     - Extract files under ``static/ninecms/ckeditor`` so that ``ckeditor.js`` is in this directory
     - A recommended ``build-config.js`` file is bundled in the above directory
     - Note: the django-ckeditor package requires a similar action too, so it is not used.

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

   - Static and Media::

       STATICFILES_DIRS = (
           os.path.join(BASE_DIR, "static"),
       )
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

       from django.contrib import messages
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
       # STATIC_ROOT = ...
       STATICFILES_DIRS = []
       CACHES = {
           'default': {
               'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
               'LOCATION': '127.0.0.1:11211',
               'TIMEOUT': 3 * 60 * 60,  # or whatever
               'KEY_PREFIX': 'myapp_',
               'VERSION': 1,
           }
       }

4. Create empty folders in project root:

   - ``/static/``
   - ``/media/``

     - *Optionally* copy the images from
       https://github.com/Wtower/django-ninecms-starter/tree/master/media/ninecms/basic/image to
       ``/media/ninecms/basic/image`` if you intend to run ninecms tests (see below).

5. Run ``./manage.py migrate`` to create the models.

6. Url configuration

   - Include the URL configurations for admin, i18n and 9cms
   - Make sure 9cms URL conf is the last line so the dynamic router catches all URLs.
   - Include ``robots.txt``
   - Include static files for local server

   URL Example::

     from django.conf import settings
     from django.conf.urls import include, url
     from django.conf.urls.i18n import i18n_patterns
     from django.conf.urls.static import static
     from django.contrib import admin
     from django.views.generic import TemplateView

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

7. Start the development server and visit http://127.0.0.1:8000/admin/

   You'll need the Admin app enabled and a superuser with ``python manage.py createsuperuser``.

8. Visit http://127.0.0.1:8000/ to view content.

9. Optionally run test with ``python manage.py test --settings=myapp.settings_test ninecms``.

From here on common tasks include:

- Theming (see below)
- Add page types
- Add content
- Add menus
- Add blocks

Theming
-------

Theming is easy and straightforward. Besides from developing a custom theme, it is easy to use any ready-made
HTML theme from the myriads available on the web.

*(Changes in v0.6.0)*

There is a ``base.html`` which gets extended by an ``index.html``. The base declares the doc type (HTML5),
loads scripts, all defined in blocks.

The index file is the one that most probably needs to be overridden. You can check the base to see where each of
the following blocks appears. These are defined by order of appearance:

- ``meta``: define any custom keywords in ``<head>``.
  Some defaults are generated based on settings and the node (page) presented.
- ``head``: define any additional elements at the bottom of the ``<head>``.
  Here add favicon and additional stylesheets / head scripts.
- ``body_attrs``: define any additional attributes to be appended to ``<body>``.
  Default is ``class`` only.
- ``body_top``: a small link to the top of the page. This is used by a small javascript to display by default
  a small fixed top link at the right bottom of the page, after having scrolled down. If it is not overridden,
  then you might need to add a ``static/ninecms/images/toplink.png`` background or custom css for ``#toplink``.
- ``body_loader``: a convenient page loader (splash screen) is defined.
  Override and leave blank if not suitable.
- ``content``: this is the main content block that needs to be overridden in index.
- ``body_bottom``: a small non-visible link at the bottom of the page.
- ``body_scripts``: define any additional content at the bottom of the ``<body>``.
  Here add additional scripts to be loaded in the end of the document.

The index file is the default template that is used, but it can be extended to be used in page types
(see theme suggestions below).

The templates in the ``ninecms/templates`` folder are examples of how to render specific contexts of blocks
and can be used either with ``{% include %}`` or can be copied into the custom templates directly.

Theme suggestions
-----------------

Each page type can have its own template. Ninecms chooses template for the page type
based in the template filename, in the following order:

- ``page_[page_type.name]``
- ``[page_type.name]``
- ``index.html``

where ``[page_type.name]`` is the machine name of the page type,
eg. if the page type name is 'Basic Page' then this will be ``basic_page``.

It is good to extend the template from index and use Django blocks at will.

Page types
----------

Page types are central to the organisation of a CMS content. In NineCMS, apart from logically organising content
to relevant page types, which can be done also with taxonomy terms, each page type can have a different page layout,
with different blocks.

Page types do not feature custom fields and thus cannot be used as the separation of entity-like models,
as eg. in Drupal. There is no intention to add such a feature as Django models can be very easily be added
in code and extend the CMS functionality.

URL aliases
-----------

Each content type can have a pre-specified default url alias for the nodes under it. If a node of that page type
does not have a url alias specified, the default will be used.

The following replacement tokens can be used:

- ``[node:id]``: The id of the node.
- ``[node:title]``: The transliterated slugified title of the node.
- ``[node:created:format]``: The date of node creation.
- ``[node:changed:format]``: The date of last node update.
- Format can be any `PHP date format`_ specifier in form
  ``(specifier)(separator)(specifier)(separator)(specifier)``, eg ``d-m-Y``.

.. _PHP date format: http://www.php.net/date

Block types
-----------

The following block types are supported:

- ``static``: Static content provided by linking to a node.
  Unlike from Drupal concept of block that defines a text fields anyway.
- ``menu``: Render a menu or submenu by linking to a menu item.
- ``signal``: Call a site-specific custom view render (see Views below).
- ``language``: Render a language switch menu.
- ``user-menu``: Render a user menu with login/logout or register links.
- ``login``: Render a login form.
- ``search``: Render a search form.
- ``search-results``: Render search results. Simple search functionality. For advanced search a proper package
  needs to be used. For a search results page add a new page type and implement the block. Case insensitive
  search cannot be done in Sqlite (see also Important points below).
- ``contact``: Render a contact form.

Views
-----

Add a new Django app in your project with ``signals.py`` to listen to the corresponding signal that is declared with
a new content block in admin.
Look at the ``ninecms/signals.py`` file on how to code the signals.

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

Front-end libraries
-------------------

*(Changes in v0.6.0)*

Front-end package management is an important aspect of any site.
In NineCMS, Libraries had been a minor convenience feature to integrate front-end packages.
It has been removed because there are already several existing possibilities than can be easily used,
most of which (even Django ones) are based on node.js.

The npm package `gulpfile-ninecms <https://github.com/Wtower/gulpfile-ninecms>_`
based on gulp has been published separately for this reason.

Image styles
------------

NineCMS allows to display images using specific styles. Some predefined styles can be found in ``ninecms/settings.py``.
These can be extended or replaced using the ``IMAGE_STYLES`` in the project's  ``settings.py``.
This is a dictionary where the index is the defined style name and its value is a dictionary with indexes ``type``
and ``value``. For example::

    IMAGE_STYLES.update({'my_style': {'type': 'thumbnail', 'size': (120, 100)}})

Possible types can be:

- ``thumbnail``: Scales an image to the smallest provided dimension.
- ``thumbnail-upscale``: Scales an image to the provided dimensions, allowing upscale.
- ``thumbnail-crop``: Crops an image to the ratio of the provided dimensions and the scales it.

The in order to use an image style in a template (eg for a ``node`` context::

    <img src="{{ node.image_set.all.0.image.url|image_style:'my_style' }}">

NineCMS uses the `Imagemagick<http://www.imagemagick.org/script/binary-releases.php>`_ library for this matter.
In order to use image styles it has to be installed on the server. When an image style for a particular image
is requested for the first time, NineCMS uses Imagemagick to create a new file in a new directory in the
initial file path with the name of the style. To refresh this file cache simply remove the directory with
the style name. Be careful not to remove the original file.

Pillow has not been used becaue at that time it had multiple issues with Python3. If a large memcache or redis is
available, `sorl-thumbnail<https://github.com/mariocesar/sorl-thumbnail>`_ may be a better solution
for high traffic web sites.

Important points
----------------

- If i18n urls: menu items for internal pages should always have language [v0.3.1a]
- Search page requires a search results block in page type and 'search' alias, requires not Sqlite [v0.4.4b]
- Add LANGUAGES in settings_test when I18N_URLS [v0.4.7b]

Footnote
--------

Any contribution to the project is highly appreciated and the best will be done to respond to it.


.. image:: https://badges.gitter.im/Wtower/django-ninecms.svg
   :alt: Join the chat at https://gitter.im/Wtower/django-ninecms
   :target: https://gitter.im/Wtower/django-ninecms?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge