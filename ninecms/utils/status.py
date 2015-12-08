""" Status utility functions """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.conf import settings
from django.core.cache import caches, cache
from django.contrib.auth.models import User
from django.core.management import call_command
from ninecms.models import Node, PageType, Image
from subprocess import call, CalledProcessError
from io import StringIO
import sys
import os
# noinspection PyPackageRequirements
import pip
import ninecms


class Capturing(list):
    """ Capture the stdout using a with statement """
    def __enter__(self):
        """ Initialise the stdout to StringIO
        Keep a reference of the initial stdout to self_stdout before
        :return: self
        """
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, *args):
        """ Reset the stdout to the initial
        :param args
        :return: None
        """
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


def version():
    """ Return the current 9cms version
    :return: a version string
    """
    return 'v%s' % ninecms.__version__


def packages():
    """ Get a list of all installed packages
    Cannot use pip.main as this prints in console and returns integer code
    :return: a list with all installed packages
    """
    return pip.get_installed_distributions()


def updates():
    """ Get a list of updates from the cache, as written by admin command check_updates
    :return: List or None
    """
    return caches['default'].get('updates')


def django_check():
    """ Perform django system checks using the admin command
    :return: a dictionary with the normal and the error outputs of the command
    """
    stdout = StringIO()
    stderr = StringIO()
    call_command('check', stdout=stdout, stderr=stderr)
    return {'stdout': stdout.getvalue(), 'stderr': stderr.getvalue()}


def django_migrations():
    """ Get all non-applied migrations
    :return: list
    """
    with Capturing() as migrations:
        call_command('showmigrations')
    return list(x for x in migrations if '[ ]' in x)


def permissions():
    """ Check permissions for certain paths or files
    :return: a list of (permission name, result)
    """
    perms = [
        ("Media folder `%s` writable" % settings.MEDIA_ROOT.split('/')[-1], os.access(settings.MEDIA_ROOT, os.W_OK)),
        ("9cms folder `ninecms` not writable", not os.access(os.path.join(settings.BASE_DIR, 'ninecms'), os.W_OK)),
        ("WSGI file `index.wsgi` not writable", not os.access(os.path.join(settings.BASE_DIR, 'index.wsgi'), os.W_OK)),
        ("Script `manage.py` not writable", not os.access(os.path.join(settings.BASE_DIR, 'manage.py'), os.W_OK)),
    ]
    for folder in settings.STATICFILES_DIRS:
        perms += [("Static folder `%s` not writable" % folder.split('/')[-1], not os.access(folder, os.W_OK))]
    for template in settings.TEMPLATES:
        for folder in template['DIRS']:  # pragma: nocover
            perms += [("Templates folder `%s` not writable" % folder.split('/')[-1], not os.access(folder, os.W_OK))]
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        perms += [(
            "Sqlite database",
            os.access(os.path.join(settings.BASE_DIR, settings.DATABASES['default']['NAME']), os.W_OK)
        )]
    return perms


def permissions_status():
    """ Return a permissions list along with a status
    Functin permissions() to become obsolete in next version
    :return: a dictionary with a perms list and a bool
    """
    perms = permissions()
    return {
        'perms': perms,
        'status': all(x[1] for x in perms)
    }


def check_command(command):
    """ Check if a command is supported
    :param command: the command to execute
    :return: boolean
    """
    try:
        call([command])
    except CalledProcessError:  # pragma: nocover
        return False
    except FileNotFoundError:  # pragma: nocover
        return False
    else:
        return True


def imagemagick_status():
    """ Check that imagemagick utilities are available
    :return: a list of (imagemagick utility, result)
    """
    return not(check_command('identify') and check_command('convert'))


def user_stat(user):
    """ Get user stats
    Use a list in loop to avoid repeating code
    Use lists for configuring loop to avoid re-typing keys
    In the loop we then zip it in a dictionary for the sake of clarity
    :return: a list of stats
    """
    u = User.objects.all()
    user_stats_config_keys = ('type', 'icon', 'url', 'url_parameters', 'queryset', 'date_field')
    user_stats_config = (
        ('users', 'user', 'admin:auth_user_changelist', '', u, 'date_joined'),
        ('staff', 'pawn', 'admin:auth_user_changelist', 'is_staff__exact=1', u.filter(is_staff=True), 'date_joined'),
        ('superusers', 'king', 'admin:auth_user_changelist', 'is_superuser__exact=1', u.filter(is_superuser=True),
         'date_joined'),
        ('nodes', 'file', 'admin:ninecms_node_changelist', '', Node.objects.all(), 'created')
    )
    if user.is_superuser:
        user_stats_config += (
            ('page types', 'book', 'admin:ninecms_pagetype_changelist', '', PageType.objects.all(), ''),
            ('images', 'camera', 'admin:ninecms_node_changelist', '', Image.objects.all(), ''),
            # ('terms', 'tags', 'admin:ninecms_taxonomyterm_changelist', '', TaxonomyTerm.objects.all(), ''),
        )
    user_stats = []
    for stat_list in user_stats_config:
        stat = dict(zip(user_stats_config_keys, stat_list))
        count = len(stat['queryset'])
        if stat['queryset'] == u:  # if qs is all users, decrease the anonymous user
            count -= 1
        last = None
        is_recent = False
        if count:
            last = stat['queryset'].latest('pk')
            last_date = getattr(last, stat['date_field'], None) if stat['date_field'] else None
            is_recent = (last_date > user.last_login) if last_date else False
        user_stats.append({
            'stat_type': stat['type'],
            'icon': stat['icon'],
            'url': stat['url'],
            'parameters': stat['url_parameters'],
            'count': count,
            'last': last,
            'is_recent': is_recent,
        })
    return user_stats


def cache_clear():
    """ Clear cache
    If not working try: (memcached only) cache._cache.flush_all()
    :return: None
    """
    cache.clear()
