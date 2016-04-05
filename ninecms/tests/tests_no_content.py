"""
Tests declaration for Nine CMS

All tests assume settings.LANGUAGE_CODE is defined
"""
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import translation
from django.conf import settings
from django.core.management import call_command
from django.core import mail
from ninecms.models import Node
from ninecms.tests.setup import assert_no_front, create_front, assert_front, create_basic, assert_basic, url_with_lang
from ninecms.management.commands.check_updates import Capturing
from ninecms.checks import check_settings
from io import StringIO
# noinspection PyPackageRequirements
import pip


class NoContentTests(TestCase):
    """ Tests with no initial content and no login """
    """ Node System """
    def test_node_view_with_no_content(self):
        """ Test node view if no content exists
        Explicitly remove url aliases if any remain, which has the same effect (see below)
        :return: None
        """
        Node.objects.all().delete()
        assert_no_front(self)

    def test_node_view_with_no_front(self):
        """ Test node view with no / alias
        :return: None
        """
        Node.objects.all().delete()
        create_front('/wrong-slug')
        assert_no_front(self)

    def test_node_view_with_front_title_not_repeating(self):
        """ Test that a front page does not repeat the title if it is the site title
        :return: None
        """
        title = settings.SITE_NAME
        create_front('/', '', title)
        response = assert_front(self, reverse('ninecms:index'), '', title)
        self.assertContains(response, '<title>' + title + '</title>', html=True)
        self.assertNotContains(response, '<title>' + title + ' | ' + title + '</title>', html=True)

    def test_node_view_with_basic_two_level(self):
        """ Test basic node, two levels in alias
        Test node view of basic page, slash is missing (expecting redirect)
        Test properly, slash is not missing
        :return: None
        """
        create_basic('about/company')
        response = assert_basic(self, 'about/company')
        self.assertRedirects(response, url_with_lang('/about/company/'), status_code=301)
        assert_basic(self, 'about/company/')

    def test_node_view_with_basic_wrong_alias(self):
        """ Test that a basic page with trailing / in alias is not found
        :return: None
        """
        create_basic('about/')
        response = self.client.get(reverse('ninecms:alias', args=('about/',)))
        self.assertEqual(response.status_code, 404)

    def test_content_node_view_with_no_content(self):
        """ Test view with no content
        :return: None
        """
        Node.objects.all().delete()
        translation.activate(settings.LANGUAGE_CODE)
        response = self.client.get(reverse('ninecms:content_node', args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_content_node_view_with_no_alias(self):
        """ Test view with a node with no path alias
        :return: None
        """
        node_revision = create_basic('')
        assert_basic(self, node_revision.node_id, 'content_node')

    def test_command_check_updates(self):
        """ Test command check updates
        :return: None
        """
        call_command('check_updates')
        with Capturing() as updates:
            pip.main(['list', '--outdated', '--retries', '1'])
        # noinspection PyUnresolvedReferences
        n = len(mail.outbox)
        if not updates:
            self.assertEqual(n, 0)  # pragma: nocover
        else:
            self.assertEqual(n, 1)  # pragma: nocover

    def test_command_cache_clear(self):
        """ Test command clear cache
        :return: None
        """
        out = StringIO()
        call_command('cache_clear', stdout=out)
        self.assertEqual(out.getvalue(), 'Cache cleared.\n')

    def test_checks(self):
        """ Test custom system checks
        :return: None
        """
        self.assertFalse(check_settings(None))

        with self.settings(
                MEDIA_ROOT=None,
                MEDIA_URL=None,
                ADMINS=None,
                MANAGERS=None,
                SESSION_COOKIE_NAME='sessionid',
                CACHES={
                    'default': {
                        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                        'KEY_PREFIX': None,
                    }
                }):
            self.assertEqual(len(check_settings(None)), 6)
