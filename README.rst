=======
NineCMS
=======

Nine CMS is a simple Django app to manage content. Users can create content and publish it to various paths.

Detailed documentation soon to be published.

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

  - Libraries
  - Character transliteration
  - Serializers
  - Custom tags
  - Basic search functionality
  - Template suggestions

- Bootstrap

Dependencies
------------

It is intented to keep the number of external dependencies as low as possible, if no significant reason is necessary.
The following are needed:

- Python (3.4+)
- Django (1.7+, 1.9 recommended): Web framework
- django-guardian (1.3+): provide per-page-type permissions
- django-mptt (0.7.4): provide trees for tags and menus
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

`:warning:` Django 1.9 notices:

- Until a new django-mptt version is released, use Django 1.8.7, or install mptt from git to avoid `mptt issue #402`_::

      pip install git+https://github.com/django-mptt/django-mptt.git

.. _mptt issue #402: https://github.com/django-mptt/django-mptt/pull/402

- Getting ``RemovedInDjango110Warning: render() must be called with a dict, not a Context.`` to a couple of places.
  Many other apps get similar warnings. Looking for solution without offending Django <1.9.

New project guide
-----------------

This is a full guide to create a new project. *Soon a Quick Guide will be added*.

There is also a project that can be used as an
`empty Django 9cms web site starter <http://www.github.com/Wtower/django-ninecms-starter>`_.

1. Create a new project

   Create a new project, if not existing, and optionally (as a reminder):

   - Create new virtualenv
   - Initialize git and initial commit

2. Dependencies

   - Add the following to the ``requirements.txt`` file::

       Django==1.9.0
       django-ninecms>=0.5.3

   - And optionally::

       coverage==4.0.3
       django-admin-bootstrapped==2.5.6
       django-admin-bootstrapped-plus>=0.1.1
       django-bootstrap3==6.2.2
       django-debug-toolbar==1.4.0
       mysqlclient==1.3.7
       newrelic==2.58.2.45
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

There is a ``base.html`` which gets extended by an ``index.html``. The base declares the doc type (HTML5),
loads scripts (from an indicative common pre-selected list as defined in settings) and defines blocks to extend
in index. For Drupal veterans it is the equivalent of ``html.tpl.php`` and it usually doesn't need to be overridden.

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

Other important template is ``site-name.html``. This is a small template to define the site name, usually
an image with logo. Unlike Drupal7, we decided to keep such one-off settings hard-coded and simple rather than
dynamic in the db.

The templates ``block_content.html`` and ``block_static.html`` fine-tune how the content is displayed.
The former loads only for the main content node as presented in index. The latter is used for any static node blocks
as defined in the administration panel (db). Optionally override them to fine tune the fields present and therefore
to reduce the number of queries executed.

In summary, override templates such as:

- ``index.html``
- ``site-name.html``
- ``block_content.html``
- ``block_static.html``

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

Page types
----------

Page types are central to the organisation of a CMS content. In NineCMS, apart from logically organising content
to relevant page types, which can be done also with taxonomy terms, each page type can have a different page layout,
with different blocks specified as elements to different regions.

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

Additionally to content of any node, which is rendered anyway (unlike from eg. Drupal that has a content block),
the following block types are supported:

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

Libraries
---------

Libraries is a minor convenience feature (discussion open) that allows to easily integrate JS scripts in the template.
A small number of files are involved: ``settings``, ``templatetags``, ``base.html``.
The implementor may select to ignore libraries and override ``base.html`` or ``index.html`` blocks for
adding scripts anyway.

Alternatively, use ``django-bower``. Bower is a front-end packages repository that by itself requires node.js,
but this package makes possible to use bower easily and install libraries easily. The downside is that proper
and sometimes plenty HTML still needs to be authored in templates, which is now handled in base.html.

Second alternative is to create (in future) and use separate django packages, such as django-bootstrap3,
and other custom package for each major widely used js package. This is nice because it deals with the
above downside with custom template tags such as ``{% bootstrap_javascript %}``, but also deals with the
requirements issue. Downside is increased maintenance for the author of them.

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
- Theme suggestions [v0.4.4b]
- Search page requires a search results block in page type and 'search' alias, requires not Sqlite [v0.4.4b]
- When serializing related field using ``table__field`` notation, always add ``select_related`` to query prior calling
  serialize [v0.4.7b]
- Add LANGUAGES in settings_test when I18N_URLS (see aluminium( [v0.4.7b]

Footnote
--------

Any contribution to the project is highly appreciated and the best will be done to respond to it.
