=========
CHANGELOG
=========

Development: v0.6.1
-------------------

Estimated release date:  May 16 2016

Update date:  Apr 11 2016

Planned changes

- Published gulpfile-ninecms project for front-end management
- Add migration 14 #46

  - remove PageLayoutElements model
  - make ContenBlock name unique not null

**:warning: Changes that require manual migration actions:**

- Upgrade to v0.6.0 prior to upgrading to future versions #45

v0.6.0
------

Date:  Apr 6 2016

What's new

- Improve page rendering #45

  - remove theme suggestions
  - use template blocks and only provide proper context
  - deprecate page layout elements
  - remove front-end libraries #43

- Admin: add m2m related fields on both ends:

  - page types / blocks
  - nodes / terms

All changes

- Integrate tests into django-ninecms repo #44
- Use Python path functions in image styles #48
- Fix #47 setup fails
- Use Travis and Coveralls #35

**:warning: Changes that require manual migration actions:**

- Upgrade all templates

  - Block rendering has changed, add relevant include statements according to readme instructions.
  - Anywhere that image styles are used, pass the actual ImageFieldFile rather than a url #48

v0.5.4
------

Date:  Sat Jan 16 2016

What's new

- Added internationalisation
- Added system checks to 9cms

All changes

- Update styles
- Fix transliterate for greek capital intonated vowels.
- Amended tests (coverage 100%)
- Internationalised 9cms

  - Migration, greek locale
  - Added translatable text to python and templates
  - Added verbose translatable names to models
  - Added global settings languages for model choices to allow migrations not to get affected by various
    projects languages setting
  - Restricted language choices in admin layer

- Fix integrity error when creating node as not super user: no default user in node user field
- Admin improvement
- Disable node clone because of Django bug
- Updates
- Allow page type to be cloned.
- Added breadcrumbs template
- Fixed regression with issue #8
- Fix menu active trail, add breadcrumbs template

  - Created small utility function to get url without language.
  - In active trail template tag, remove language part from url if i18n urls are enabled
  - Previously, if language in url, the query would not work well.
  - Fixes issue with not recognising active trail.

- If page type is immediately repeated (same block more than once in one page type), add '+' instead
- Added context to signals by providing the node object in display.
- Fixed regression in #11 and bumped version to 0.5.3.1 for PyPi.

v0.5.3
------

Date:   Wed Dec 9 2015

What's new

- Added feature: remove uploaded file (and any image styles-thumbnails) when the relevant record is removed.
- Improved documentation
- Improvements
- Upgraded to Django 1.9

All changes

- Fix #11
- Added help texts to models with reference to documentation
- Added images to the project
- Added more blocks in ``base.html``.
- Fixes #8
- Added feature: remove uploaded file (and any image styles-thumbnails) when the relevant record is removed.
- Added pre-delete signal.
- It appears that multiple pre-delete functions with decorators do not get called, so merged function with
  previous ``delete_guardian_group_perms``.
- Using added function in media.py to search for all files with the same name, below the path, in order to trace
  all thumbnails and then remove all.
- Updated tests to cover new feature.
- Minor update in readme.
- Modified code that returns the path of an uploaded media file be OS-agnostic
- Improved test to allow different title in admin (still containing "administration")
- Improved documentation
- Added class to index.html to improve navigation in inspector
- Added reference to django-ninecms-starter on readme
- Improved documentation

v0.5.2
------

Date:   Wed Nov 25 2015

What's new

- Package fixes

All changes

- Bumped minor version from v0.5.2 to v0.5.2.2 to update pypi.
- Fixed manifest to include all subpackages in python setup.
- Fixed tests to respect current language.
- Fixed issue in admin.py
- Cannot redirect within ``formfield_for_foreignkey`` as we need to return whatever parent returns and not an
  http response.
- Removed redundant code as in the interface there is a button to add page types anyway.
- Merge pull request #6 from Wtower/docs
- Fix setup.py
- Removed incorrectly added ``docs`` from ``setup.py``
- Bumped version 0.5.2 to allow pypi upload.

v0.5.1
------

Date:   Wed Nov 25 2015

What's new

- Deploy as PyPi package
- Improvements on documentation

All changes

- Merge pull request #5 from Wtower/docs
- Improvements on documentation
- Reflecting newly created pypi package
- Bumped version 0.5.1
- Merge pull request #4 from Wtower/docs
- Added screenshots
- Minor changes in git ignore, setup.py
- Merge pull request #3 from Wtower/documentation
- Fixes #2

v0.5.0
------

Date:   Tue Nov 17 2015

What's new

- First release in GitHub

All changes

- Merge branch 'master' of https://github.com/Wtower/django-ninecms
- Added MANIFEST.in
- Added setup.py
- Initial commit in new repo

v0.4.9b
-------

Date:   Thu Nov 12 2015

What's new

- Improved admin UI
- Improved status page
- Improvements

All changes

- Add UI video, files formsets, perms, tests
- Upgrade admin site
- Use bootstrap instead of grappelli
- Guardian perms: bug in guardian not allows use admin
- Custom templates and javascript:
- CKeditor implemented by overriding change_form.html
- Base html requires an additional app before d-a-b in order to be overridden to utilize sb-admin
- Status page in front page possibly: Node / user numbers in 4 boxes etc
- Possibly override admin save to clean data / custom validate: use custom modelform
- Set initial data
- Admin site name
- Admin urls in page type admin
- Status page: Add comments (check_updates)
- Remove commented out code from permission checks of previous revision (models, forms, views, templates, tests)
- Moved class Capturing to status
- Added django check command output
- Added django show migrations command output
- Notice: On settings add TEMPLATE_DIRS for PyCharm and unset in settings_live.
- Added command cache_clear, test
- Fix issue with url alias when suffixing existing alias for different language (models)
- Fix issue when adding new node as superuser and no page types, to redirect to add page type instead of 403 (views)
- Updates commented-out settings
- Add library angularjs
- Added link when no user groups are available in content type add/edit permissions
- Fix issue in sanitize.py: strip_tags(None) throws exception.

**:warning: Changes that require manual migration actions:**

- Remove grappelli (settings, pip, urls)
- Add django-admin-bootstrapped (settings, pip)
- Add django-admin-bootstrapped-plus (settings)
- Add bootstrap3 (pip)

v0.4.8b
-------

Date:   Tue Nov 3 2015

What's new

- Status page
- Permissions per content type
- Improvements

All changes

- Speed up query (render)
- Change text in content (templates)
- Implement url alias pattern (models)
- Status page (commands, templates, utils, urls, views)
- Permissions per content type (templates, utils, forms, views)
- Tests
- Add get parameters in contact form render (utils)
- Allow attributes for td, th sanitize (utils)
- Improve thumbnail-crop (utils)
- Upgraded ckeditor
- Minor refactoring (utils)
- Fixed minor issue (tests)
- Added order_by to ContentView (views)
- Added permission: Node: view unpublished (models, views, utils, css, migrations)
- Transliterate path_file_name (utils/media, migrations)
- Added ``<br>`` tag (utils/sanitize)
- Upgraded libraries (templates)
- Amended tests

**:warning: Changes that require manual migration actions:**

- Add KEY_PREFIX_ and VERSION_ in memcached setting

.. _KEY_PREFIX: http://docs.djangoproject.com/en/1.8/topics/cache/#cache-key-prefixing
.. _VERSION: http://docs.djangoproject.com/en/1.8/topics/cache/#cache-versioning

v0.4.7b
-------

Date:   Tue Sep 22 2015

What's new

- Improvements

All Changes

- Improvements on serializer (utils)
- Added more local libraries (settings, templates)
- Fixed issue in image_style (utils)
- Using glyphicons in content admin (templates)
- Added pagination in content (templates)
- Fixed affix issue (templates, js)
- Added glyphicon tag (templatetags)
- Change construct_classes (views)
- Added edit inline in content list (forms, views, templates, js, css)
- Change block search, results (templates)
- Streamlined block_render (utils)
- Amended block_menu_header (templates)
- Amended tests
- Moved NodeView (views, utils)
- Added ExtBaseSerializer (utils)
- Added owl carousel (settings, templates)

**:warning: Changes that require manual migration actions:**

- Add TEMPLATES in settings_test without DIRS and in settings_live without ``debug``.
- Add PASSWORD_HASHERS in settings_test to `speed up tests`_ (10%)
- Migrate

.. _speed up tests: http://docs.djangoproject.com/en/1.4/topics/testing/#speeding-up-the-tests

v0.4.6b
-------

Date:   Wed Sep 2 2015

What's new

- Libraries improvements
- Other improvements

All changes

- Page elements order by id (views)
- Libraries improvements in loader, pagetop, script order, affix, messages, wow (settings, templates, css, js)

v0.4.5b
-------

Date:   Thu Aug 27 2015

What's new

- Improvements

All changes

- Various amendments (templatetags)
- Security fix (urls)
- Removed parent field (admin)
- Improved block render template selection, classes, menu rendering (views)
- Amended TaxonomyTerm (models, migrations)
- Amended styles (css)
- Amended tests coverage for page types forms
- Reorganized tests into multiple files

v0.4.4b
-------

Date:   Wed Jul 29 2015

What's new

- Added block login form
- Added block user menu
- Added block search form
- Added block search results
- Improvements

All changes

- Added meta description, author, keywords (settings, views, templates)
- Changed default values in node add form (views)
- Used field custom tag (block_contact_form)
- Added active trail (templatetags, templates)
- Amended tests
- Fixed variable name (views)
- Removed unique together from page layout elements (models)
- Added blocks for login and user menu (templates, views)
- Added search box and results (templates, views)
- Added content type interface (forms, views, templates)
- Added iosSlider in libraries
- Moved image_style to media (templatetags, utils)
- Amended tests
- Added hidden field in page layout elements (models, views, migrations)
- Added upper_no_intonation filter (extratags, utils)
- Added cancel link in form_node (templates)
- Added utility classes (css)

**:warning: Changes that require manual migration actions:**

- Check any site that uses contact form, that it uses ``{% field %}`` in overridden blocks,
  and that it renders properly
- Migrate

v0.4.3b
-------

Date:   Thu Jun 25 2015

What's new

- Nodes user interface
- Improvements on permissions
- Other improvements

All changes

- Refactoring (models, forms into utils)
- Added permissions (models, urls, views, migrations, templates)
- Minor changes (models, migrations)
- Added fields, formset, ajax support (forms, templatetags, templates, js)
- Added node delete, content types page (urls, views, templates)
- Added contrib.messages (views)
- Default form values (views)
- Amendments (tests)
- Upgraded bootstrap (templates, static)

**:warning: Changes that require manual migration actions:**

- Install guardian
- For external modules: ``transliterate`` moved to utils
- Migrate

v0.4.2b
-------

Date:   Mon Jun 15 2015

What's new

- Improvements

All changes

- Minor improvement in extratag, base
- Added robots.txt
- Added favicon.ico
- Added language menu block (views, templates, css)
- Added messages contrib (views, templates)
- Added node clone view (views, templates)
- Added ckeditor.html
- Added comments on settings
- Content blocks interface improvement (admin)
- Minor improvement in html sanitize (forms, tests)

**:warning: Changes that require manual migration actions:**

- Remove console from index.html
- Add robots.txt in urls.py
- Add favicon.ico in index.html
- Install grappelli

v0.4.1b
-------

Date:   Fri May 29 2015

What's new

- Improvements on permissions
- Other improvements

All changes

- Minor migration
- Permissions: ckeditor proper configuration (templates)
- Html sanitize (forms, views, tests)
- Fixed minor error in models
- Minor comments

**:warning: Changes that require manual migration actions:**

- Install bleach
- Migrate

v0.4.0b
-------

Date:   Thu Apr 30 2015

What's new

- First Beta version
- Added transliterate feature
- Improvements

All changes

- Introduced default settings
- Added library waypoints
- Several fixes
- Transliteration
- Configured ckeditor in node edit (templates)
- Squashed migrations
- Amended tests for node alias template
- Improved menu template

**:warning: Changes that require manual migration actions:**

- Migrate

v0.3.3a
-------

Date:   Fri Apr 17 2015

What's new

- Improvements

All changes

- Nodes: url alias (models, admin, views, forms, tests, templates, custom migration)
- Improve admin for nodes
- Added classes render for blocks (views, templates)
- Dismissed test for image (no coverage)

**:warning: Changes that require manual migration actions:**

- Migrate

v0.3.2a
-------

Date:   Wed Apr 15 2015

What's new

- Added custom permissions
- Node redirect
- Improvements

All changes

- Nodes: url alias redirect, get absolute url (models, admin, views, tests, templates)
- Permissions: toolbar, full html (models, views, templates)
- Improvements: updates urls.py to remove patterns() for Django 1.8
- Libraries: updated bootstrap local, jquery.scrollto local, video.js local
- Improved base.html
- Nodes: added full_path for url alias (models, tests)
- Changed order in meta declaration (models)
- Improved templates

v0.3.1a
-------

Date:   Thu Apr 9 2015

What's new

- Improvements on menus
- Other improvements
- Upgraded to Python 3.4
- Upgraded to Django 1.8 LTS

All changes

- Reorganized tests based on setUp
- Added top-link, menu bookmark scroll (static, templates)
- Menu system improvements (models, admin, views, tests, templates)
- Upgraded to Python3 (apps, models, views, templatetags, migrations)
- Upgraded to Django 1.8 (models, urls, migrations)
- Upgraded to MPTT 0.7.1 (views)
- Amended tests to cover 100% (tests, views)
- Tests: allowed multiple languages handling, different current language.

v0.3.0a
-------

Date:   Wed Apr 1 2015

What's new

- Introduced libraries feature
- Improvements on image styles
- Other improvements

All changes

- Libraries system (templatetags, templates, settings, static files)
- Updated tests
- Minor template and style updates

**:warning: Changes that require manual migration actions:**

- Make changes in project settings for 9cms changes and Django 1.8.

v0.2.5pa
--------

Date:   Fri Mar 27 2015

What's new

- Added contact form
- Taxonomy improvements
- Views improvements
- Other improvements

Minor changes

- Added contact form system (models, urls, forms, views, templates)
- Added console messaging system (views, templates)
- Added link field in nodes (models, forms, templates)
- Identified node add bug (views)
- Migrations

**:warning: Changes that require manual migration actions:**

- Many features introduced, check existing projects thoroughly
- Migrate

v0.2.4pa
--------

Date:   Thu Mar 26 2015

What's new

- Added image styles
- Improvements

All changes

- Media system: image styles
- Fixed fieldset bootstrap issue in form_node
- Added head and body scripts blocks, Bootstrap from CDN in base.html
- Added missing form_node and signals from previous commits
- Fixed image inline formset issue with missing id in content form
- Added page-header class in templates

v0.2.3pa
--------

Date:   Tue Mar 24 2015

What's new

- Added video field
- Added CKEditor
- Improvements

All changes

- Improved node content forms: added image inline formset, theme
- Minor improvements in style.css, views
- Separated signals.py
- Improved content list/edit/add theme
- Refactored NodeView to construct classes in member function
- Changed Content Node Edit / Add views
- Improved content administration templates for bootstrap
- Added CKEditor support
- Theming improvements: shrinkable navbar (layout.js, style.css)
- Added classes, title in body from render_page (base.html, views.py)
- Made toolbar fixed, clean-up (base.html)
- Improved block_content.html, index.html
- Added default block_signal.html
- Media system: improved, added video (models.py, admin.py, tests.py)
- Added custom view random node videos (views.py, templates)

v0.2.2pa
--------

Date:   Tue Mar 17 2015

What's new

- Added signals (views)
- Improvements

All changes

- Improved style.css
- Added extend.css and layout.js
- Improved bootstrap in templates (base, menu, index)
- Fixed menu model full path
- Added template suggestions in views render page and in templates
- Amended tests
- Added Signal System (models, views, templates, migrations, fixtures, tests)
- Added separate settings file for tests in sqlite3

v0.2.1pa
--------

Date:   Mon Mar 9 2015

What's new

- Added taxonomy
- Improvements

All changes

- Added Taxonomy System (models, admin, views, templates, migrations, fixtures, tests)
- Removed commented out code
- Amended menu system model
- Minor fix in menu system admin
- Streamlined and restructured views
- Added status and disabled check in page render in views
- Amended menu template

v0.2.0pa
--------

Date:   Mon Mar 9 2015

What's new

- Started project anew
- Added nodes
- Added blocks
- Added media
- Added menu

All changes

- Re-organized Node System (models, admin, views, forms, tests, templates)
- Added docstring comments project-wide
- Towards permanent remove of commented out code
- Tests for menu system
- Tested several options for node system; Towards node system redesign
- Added menu system (models, migrations, dump data, admin, views, template)
- Added mptt and debug-toolbar
- Optimized queries (from 15 to 12 called for index)
- Towards render menu title
- Tests
- Possible change in node system for better queries

**:warning: Changes that require manual migration actions:**

- Redesigned all system, no backwards compatibility

v0.1.3pa
--------

Date:   Mon Mar 2 2015

What's new

- Added media
- Added menu
- Improvements

All changes

- Added media system (migrations, models, admin, urls, settings, template, tests)
- Reinstated slug check for / in views. urls
- Minor streamline in views
- Moved get_latest_node_revision to models
- Implemented get_latest_node_revision_or_404 to NodeView in views
- NodeView is now super-class
- Streamlined views to accommodate new funcs
- Amended tests

v0.1.2pa
--------

Date:   Sat Feb 28 2015

What's new

- Improvements on blocks
- Other improvements

All changes

- Cleaned and streamlined files to prepare for Media system
- Block system stable
- Changed get_blocks to page_render and added templates
- Amended tests
- Signed templates
- Nightly commit: blocks prior to changing render from dict-based to region-based
- Also changing index.html iteration

v0.1.1pa
--------

Date:   Thu Feb 26 2015

What's new

- Started project
- Added nodes
- Added blocks

All changes

- Blocks system (models)
- Initial commit

Version requirements

- Python 2.7
- Django 1.7
