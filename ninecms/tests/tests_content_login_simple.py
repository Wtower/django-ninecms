"""
Tests declaration for Nine CMS

All tests assume settings.LANGUAGE_CODE is defined
"""
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.test import TestCase
from django.contrib.auth.models import Permission, Group
from django.core.urlresolvers import reverse
from ninecms.tests.setup import create_front, create_basic, create_simple_user, create_image, data_node
from ninecms.utils.perms import set_perms
from ninecms.forms import ContentTypePermissionsForm, ContentNodeEditForm


class ContentLoginSimpleTests(TestCase):
    """ Tests for access, with content, with login from simple user
    The first page (front) is allowed to be edited by simple user
    The second is not.
    """
    @classmethod
    def setUpTestData(cls):
        """ Setup initial data:
        Create front page
        Create basic page
        Create simple user
        Create image
        :return: None
        """
        cls.node_rev_front = create_front('/')
        cls.node_rev_basic = create_basic('about')
        cls.simple_user = create_simple_user()
        cls.simple_group = Group.objects.create(name='editor')
        cls.simple_user.groups.add(cls.simple_group)
        perms = Permission.objects.filter(codename__in=['add_node', 'change_node'])
        cls.simple_user.user_permissions.add(*perms)
        cls.default_perms = {
            'change_node': [cls.simple_group],
            'delete_node': [],
            'add_node': [cls.simple_group],
        }
        cls.fields = list(ContentTypePermissionsForm().fields.keys())
        cls.img = create_image()

    def setUp(self):
        """ Setup each test: login
        :return: None
        """
        self.client.login(username='editor', password='1234')

    """ Admin index """
    def test_admin_index_page(self):
        """ Test status page
        :return: None
        """
        response = self.client.get(reverse('admin:index'))
        self.assertContains(response, "administration")
        self.assertContains(response, '<span class="stat-count-users h1">')
        self.assertContains(response, '<span class="stat-count-staff h1">')
        self.assertContains(response, '<span class="stat-count-superusers h1">')
        self.assertContains(response, '<span class="stat-count-nodes h1">')
        self.assertNotContains(response, '<span class="stat-count-page-types h4">')
        self.assertNotContains(response, '<span class="stat-count-images h4">')
        self.assertNotContains(response, "Utilities")

    """ Nodes """
    def test_admin_node_changelist_page(self):
        """ Test view /admin/ninecms/node/ properly
        :return: None
        """
        response = self.client.get(reverse('admin:ninecms_node_changelist'))
        self.assertEqual(response.status_code, 403)
        perms = {'add_node': [self.simple_group], 'change_node': [self.simple_group], 'delete_node': []}
        obj = self.node_rev_basic.node.page_type
        set_perms(obj, self.fields, '_pagetype', perms)
        response = self.client.get(reverse('admin:ninecms_node_changelist'))
        self.assertContains(response, "Basic Page")
        self.assertNotContains(response, "Clear cache")
        self.assertNotContains(response, '<option value="delete_selected">')

    def test_admin_node_change_page(self):
        """ Test that renders properly /admin/ninecms/node/<node_id>/
        Get the basic page to test image as well
        Also test fields exclusive to superuser
        Check that user field populates only with current user
        Notice that here the field is not selected as there is a different user for this node, not present in queryset
        :return: None
        """
        response = self.client.get(reverse('admin:ninecms_node_change', args=(self.node_rev_basic.node_id,)),
                                   follow=True)
        self.assertEqual(response.status_code, 404)  # this returns a 404
        perms = {'add_node': [self.simple_group], 'change_node': [self.simple_group], 'delete_node': []}
        obj = self.node_rev_basic.node.page_type
        set_perms(obj, self.fields, '_pagetype', perms)
        response = self.client.get(reverse('admin:ninecms_node_change', args=(self.node_rev_basic.node_id,)))
        self.assertContains(response, ('<input class="form-control vTextField" id="id_title" maxlength="255" '
                                       'name="title" placeholder="Title" required="required" title="" type="text" '
                                       'value="%s">' % self.node_rev_basic.node.title), html=True)
        self.assertNotContains(response, '<label for="id_alias">Alias:</label>', html=True)
        self.assertNotContains(response, '<label class="vCheckboxLabel" for="id_redirect">Redirect</label>', html=True)
        self.assertContains(response, ('<select class="form-control form-control-inline" id="id_user" name="user" '
                                       'title=""><option value="">---------</option>'
                                       '<option value="%d">%s</option>'
                                       '</select>' % (self.simple_user.pk, self.simple_user.username)), html=True)

    def test_admin_node_add_page(self):
        """ Test that renders properly /admin/ninecms/node/add/
        Also test fields exclusive to superuser
        Also test initial data
        Check that user field populates only with current user
        Notice that here the user field is selected by form initial data
        :return: None
        """
        response = self.client.get(reverse('admin:ninecms_node_add'))
        self.assertEqual(response.status_code, 403)
        perms = {'add_node': [self.simple_group], 'change_node': [self.simple_group], 'delete_node': []}
        obj = self.node_rev_basic.node.page_type
        set_perms(obj, self.fields, '_pagetype', perms)
        response = self.client.get(reverse('admin:ninecms_node_add'))
        self.assertNotContains(response, '<label for="id_alias">Alias:</label>', html=True)
        self.assertNotContains(response, '<label class="vCheckboxLabel" for="id_redirect">Redirect</label>', html=True)
        self.assertContains(response, ('<select class="form-control form-control-inline" id="id_user" name="user" '
                                       'title=""><option value="">---------</option>'
                                       '<option value="%d" selected="selected">%s</option>'
                                       '</select>' % (self.simple_user.pk, self.simple_user.username)), html=True)
        self.assertContains(response, ('<input checked="checked" class="" id="id_status" name="status" type="checkbox" '
                                       'value="1">'), html=True)
        self.assertContains(response, '<input class="" id="id_promote" name="promote" type="checkbox">', html=True)
        self.assertNotContains(response, ('<input checked="checked"  class="" id="id_promote" name="promote" '
                                          'type="checkbox">'), html=True)
        self.assertContains(response, '<input class="" id="id_sticky" name="sticky" type="checkbox">', html=True)
        self.assertNotContains(response, ('<input checked="checked"  class="" id="id_sticky" name="sticky" '
                                          'type="checkbox">'), html=True)

    def test_content_node_edit_form_valid(self):
        """ Test that a form is valid
        :return: None
        """
        data = data_node(self.node_rev_front.node.page_type_id, self.simple_user)
        form = ContentNodeEditForm(data=data, user=self.simple_user)
        r = form.is_valid()
        self.assertEqual(r, True)
        self.assertEqual(form.cleaned_data['body'],
                         '&lt;div&gt; &lt;/div&gt;&lt;script&gt;alert("This is a test.");&lt;/script&gt;')

    """ Permissions: utility functions """
    def test_utils_perms(self):
        """ Test guardian and utility permissions
        Performed in a single test in order to cover changes from multiple states
        :return: None
        """
        obj = self.node_rev_basic.node.page_type
        # test set empty
        perms = {'change_node': [], 'delete_node': [], 'add_node': []}
        set_perms(obj, self.fields, '_pagetype', perms)
        self.assertFalse(self.simple_user.has_perm('change_node_pagetype', obj))
        self.assertFalse(self.simple_user.has_perm('delete_node_pagetype', obj))
        self.assertFalse(self.simple_user.has_perm('add_node_pagetype', obj))
        # test set existing
        perms = {'change_node': [], 'delete_node': [], 'add_node': [self.simple_group]}
        set_perms(obj, self.fields, '_pagetype', perms)
        self.assertFalse(self.simple_user.has_perm('change_node_pagetype', obj))
        self.assertFalse(self.simple_user.has_perm('delete_node_pagetype', obj))
        self.assertTrue(self.simple_user.has_perm('add_node_pagetype', obj))
        # test set/unset
        perms = {'change_node': [self.simple_group], 'delete_node': [], 'add_node': []}
        set_perms(obj, self.fields, '_pagetype', perms)
        self.assertTrue(self.simple_user.has_perm('change_node_pagetype', obj))
        self.assertFalse(self.simple_user.has_perm('delete_node_pagetype', obj))
        self.assertFalse(self.simple_user.has_perm('add_node_pagetype', obj))
