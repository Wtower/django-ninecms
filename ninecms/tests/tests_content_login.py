"""
Tests declaration for Nine CMS

All tests assume settings.LANGUAGE_CODE is defined

Sections index
- Admin index
- Nodes
- Page types
- Content blocks
- Menus
- Logout
- Permissions
- Status page
"""
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
# noinspection PyPackageRequirements
from guardian.models import GroupObjectPermission
from ninecms.forms import ContentNodeEditForm, ImageForm, FileForm, VideoForm, PageTypeForm
from ninecms.tests.setup import create_front, create_basic, create_user, create_image, create_block_simple, \
    get_front_title, assert_front, data_login, data_node, get_basic_title, create_video, create_file, data_page_type, \
    create_terms
from ninecms.models import PageType, Node, PageLayoutElement, ContentBlock, TaxonomyTerm
import os


class ContentLoginTests(TestCase):
    """ Tests with content, with login """
    @classmethod
    def setUpTestData(cls):
        """ Setup initial data:
        Create front page
        Create basic page
        Create user
        Create image
        :return: None
        """
        cls.node_rev_front = create_front('/')
        cls.node_rev_basic = create_basic('about')
        cls.admin = create_user()
        cls.simple_group = Group.objects.create(name='editor')
        cls.img = create_image()
        cls.block_login = create_block_simple(cls.node_rev_front.node.page_type, 'login')
        cls.block_user_menu = create_block_simple(cls.node_rev_front.node.page_type, 'user-menu')
        # add a second user menu element in same page type
        PageLayoutElement(
            page_type=cls.node_rev_front.node.page_type,
            region='footer',
            block=cls.block_user_menu,
            weight=0).save()

    def setUp(self):
        """ Setup each test: login
        :return: None
        """
        self.client.login(username=self.admin.username, password='1234')

    """ Admin index """
    def test_admin_index_page(self):
        """ Test status page
        :return: None
        """
        response = self.client.get(reverse('admin:index'))
        self.assertContains(response, "administration")
        # Users
        self.assertContains(response, '<span class="stat-count-users h1">1</span>', html=True)
        self.assertContains(response, ('<span class="stat-latest-users">'
                                       'Latest: <a href="/admin/auth/user/">admin</a></span>'), html=True)
        # Staff users
        self.assertContains(response, '<span class="stat-count-staff h1">1</span>', html=True)
        self.assertContains(response, ('<span class="stat-latest-staff">'
                                       'Latest: <a href="/admin/auth/user/">admin</a></span>'), html=True)
        # Superusers
        self.assertContains(response, '<span class="stat-count-superusers h1">1</span>', html=True)
        self.assertContains(response, ('<span class="stat-latest-superusers">'
                                       'Latest: <a href="/admin/auth/user/">admin</a></span>'), html=True)
        # Nodes
        self.assertContains(response, '<span class="stat-count-nodes h1">2</span>', html=True)
        self.assertContains(response, ('<span class="stat-latest-nodes">'
                                       'Latest: <a href="/admin/ninecms/node/">'
                                       '%s</a></span>' % get_basic_title(settings.LANGUAGE_CODE, '')), html=True)
        # Page types
        self.assertContains(response, '<span class="stat-count-page-types h4">2</span>', html=True)
        self.assertContains(response, ('<span class="stat-latest-page-types">'
                                       'Latest: <a href="/admin/ninecms/pagetype/">Basic Page</a></span>'), html=True)
        # Images
        self.assertContains(response, '<span class="stat-count-images h4">1</span>', html=True)
        self.assertContains(response, ('<span class="stat-latest-images">'
                                       'Latest: <a href="/admin/ninecms/node/">'
                                       '%s</a></span>' % get_basic_title(settings.LANGUAGE_CODE, '')), html=True)
        # Other status
        self.assertRegex(response.content.decode(), '<div id="panel-updates"[\W\s]+class="panel panel-success">')
        self.assertRegex(response.content.decode(), '<div id="panel-migrations"[\W\s]+class="panel panel-success">')
        self.assertRegex(response.content.decode(), '<div id="panel-imagemagick"[\W\s]+class="panel panel-success">')
        self.assertContains(response, "Utilities")

    """ Node System """
    def test_admin_node_changelist_page(self):
        """ Test view /admin/ninecms/node/ properly
        :return: None
        """
        response = self.client.get(reverse('admin:ninecms_node_changelist'))
        self.assertContains(response, get_front_title())
        self.assertContains(response, "Clear cache")
        self.assertContains(response, '<option value="delete_selected">')

    def test_admin_node_change_page(self):
        """ Test that renders properly /admin/ninecms/node/<node_id>/
        Get the basic page to test image as well
        Also test fields exclusive to superuser
        :return: None
        """
        response = self.client.get(reverse('admin:ninecms_node_change', args=(self.node_rev_basic.node_id,)))
        self.assertContains(response, ('<input class="form-control vTextField" id="id_title" maxlength="255" '
                                       'name="title" placeholder="Title" required="required" title="" type="text" '
                                       'value="%s">' % self.node_rev_basic.node.title), html=True)
        self.assertContains(response, '<div class="node-image-inline thumbnail">')
        self.assertContains(response, '<label for="id_alias">Alias:</label>', html=True)
        self.assertContains(response, '<label class="vCheckboxLabel" for="id_redirect">Redirect</label>', html=True)
        self.assertContains(response, '<label class="required" for="id_user">')

    def test_admin_node_add_page(self):
        """ Test that renders properly /admin/ninecms/node/add/
        Also test fields exclusive to superuser
        Also test initial data
        :return: None
        """
        response = self.client.get(reverse('admin:ninecms_node_add'))
        self.assertContains(response, '<label for="id_alias">Alias:</label>', html=True)
        self.assertContains(response, '<label class="vCheckboxLabel" for="id_redirect">Redirect</label>', html=True)
        self.assertContains(response, '<label class="required" for="id_user">')
        self.assertContains(response, 'selected="selected">admin</option>')
        self.assertContains(response, ('<input checked="checked" class="" id="id_status" name="status" type="checkbox" '
                                       'value="1">'), html=True)
        self.assertContains(response, '<input class="" id="id_promote" name="promote" type="checkbox">', html=True)
        self.assertNotContains(response, ('<input checked="checked"  class="" id="id_promote" name="promote" '
                                          'type="checkbox">'), html=True)
        self.assertContains(response, '<input class="" id="id_sticky" name="sticky" type="checkbox">', html=True)
        self.assertNotContains(response, ('<input checked="checked"  class="" id="id_sticky" name="sticky" '
                                          'type="checkbox">'), html=True)

    def test_content_node_edit_form_invalid(self):
        """ Test that an empty form is invalid
        :return: None
        """
        form = ContentNodeEditForm()
        self.assertEqual(form.is_valid(), False)

    def test_content_node_edit_form_valid(self):
        """ Test that a form is valid
        :return: None
        """
        data = data_node(self.node_rev_front.node.page_type_id, self.admin)
        form = ContentNodeEditForm(data=data, user=self.admin)
        r = form.is_valid()
        self.assertEqual(r, True)
        self.assertEqual(form.cleaned_data['body'],
                         '<div> </div>&lt;script&gt;alert("This is a test.");&lt;/script&gt;')

    def test_content_node_edit_form_m2m_valid(self):
        """ Test that a node form's reverse m2m is valid
        :return: None
        """
        create_terms(())
        # assign 2 tags
        data = data_node(self.node_rev_front.node.page_type_id, self.admin)
        data['terms'] = (1, 2)
        form = ContentNodeEditForm(data=data, user=self.admin)
        r = form.is_valid()
        self.assertEqual(r, True)
        self.assertEqual(list(form.cleaned_data['terms']), list(TaxonomyTerm.objects.all()))
        form.save()
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(len(form.instance.terms.all()), 2)

        # remove 1 tag
        data['terms'] = (1,)
        form = ContentNodeEditForm(data=data, user=self.admin, instance=form.instance)
        r = form.is_valid()
        self.assertEqual(r, True)
        form.save()
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(len(form.instance.terms.all()), 1)

    def test_image_form_valid_sanitize(self):
        """ Test forms sanitize; Test image form
        Form is invalid as it requires image filename etc.
        :return: None
        """
        data = {'title': '<strong>test</strong>'}
        for form in (ImageForm(data=data), FileForm(data=data), VideoForm(data=data)):
            self.assertEqual(form.is_valid(), False)
            self.assertEqual(form.cleaned_data['title'], 'test')

    def test_image_delete(self):
        """ Test that files are deleted when a media is deleted
        :return: None
        """
        obj = create_image('media_delete.jpg')
        path = obj.image.path
        # create_path_file(path)
        open(path, 'a').close()
        self.assertTrue(os.path.isfile(path))
        obj.delete()
        self.assertFalse(os.path.isfile(path))

    def test_video_delete(self):
        """ Test that files are deleted when a media is deleted
        :return: None
        """
        obj = create_video('ninecms/basic/image/media_delete.jpg')
        path = obj.video.path
        open(path, 'a').close()
        self.assertTrue(os.path.isfile(path))
        obj.delete()
        self.assertFalse(os.path.isfile(path))

    def test_file_delete(self):
        """ Test that files are deleted when a media is deleted
        :return: None
        """
        obj = create_file('ninecms/basic/image/media_delete.txt')
        path = obj.file.path
        open(path, 'a').close()
        self.assertTrue(os.path.isfile(path))
        obj.delete()
        self.assertFalse(os.path.isfile(path))

    def test_admin_node_action_node_publish(self):
        """ Test admin action node publish
        :return: None
        """
        data = {'action': 'node_unpublish', '_selected_action': Node.objects.all().values_list('pk', flat=True)}
        response = self.client.post(reverse('admin:ninecms_node_changelist'), data, follow=True)
        self.assertContains(response, "nodes successfully updated as not published")
        self.assertEqual(Node.objects.filter(status=True).count(), 0)
        data['action'] = 'node_publish'
        response = self.client.post(reverse('admin:ninecms_node_changelist'), data, follow=True)
        self.assertContains(response, "nodes successfully updated as published")
        self.assertEqual(Node.objects.filter(status=False).count(), 0)

    def test_admin_node_action_node_promote(self):
        """ Test admin action node promote
        :return: None
        """
        data = {'action': 'node_promote', '_selected_action': Node.objects.all().values_list('pk', flat=True)}
        response = self.client.post(reverse('admin:ninecms_node_changelist'), data, follow=True)
        self.assertContains(response, "nodes successfully updated as promoted")
        self.assertEqual(Node.objects.filter(promote=False).count(), 0)
        data['action'] = 'node_demote'
        response = self.client.post(reverse('admin:ninecms_node_changelist'), data, follow=True)
        self.assertContains(response, "nodes successfully updated as not promoted")
        self.assertEqual(Node.objects.filter(promote=True).count(), 0)

    def test_admin_node_action_node_sticky(self):
        """ Test admin action node sticky
        :return: None
        """
        data = {'action': 'node_sticky', '_selected_action': Node.objects.all().values_list('pk', flat=True)}
        response = self.client.post(reverse('admin:ninecms_node_changelist'), data, follow=True)
        self.assertContains(response, "nodes successfully updated as sticky")
        self.assertEqual(Node.objects.filter(sticky=False).count(), 0)
        data['action'] = 'node_unsticky'
        response = self.client.post(reverse('admin:ninecms_node_changelist'), data, follow=True)
        self.assertContains(response, "nodes successfully updated as not sticky")
        self.assertEqual(Node.objects.filter(sticky=True).count(), 0)

    def test_admin_node_action_node_reset_alias(self):
        """ Test admin action node sticky
        :return: None
        """
        data = {'action': 'node_reset_alias', '_selected_action': Node.objects.all().values_list('pk', flat=True)}
        response = self.client.post(reverse('admin:ninecms_node_changelist'), data, follow=True)
        self.assertContains(response, "nodes successfully updated")

    """ Page types """
    def test_admin_page_type_changelist_page(self):
        """ Test that page type changelist page renders properly
        :return: None
        """
        response = self.client.get(reverse('admin:ninecms_pagetype_changelist'))
        self.assertContains(response, '<th class="field-name"><a href="%s">%s</a></th>' % (
            reverse('admin:ninecms_pagetype_change', args=(self.node_rev_basic.node.page_type_id,)),
            self.node_rev_basic.node.page_type.name))

    def test_admin_page_type_change_page(self):
        """ Test that page type change page renders properly
        :return: None
        """
        response = self.client.get(reverse('admin:ninecms_pagetype_change',
                                           args=(self.node_rev_basic.node.page_type_id,)))
        # with open('response.html', 'w') as out:
        #     out.write(response.content.decode())
        self.assertContains(response, '<input class="form-control vTextField" id="id_name" maxlength="100" '
                                      'name="name" placeholder="Name"')
        self.assertContains(response, '<select multiple="multiple" class="selectfilterstacked" '
                                      'id="id_blocks" name="blocks" title="">')

    def test_content_page_type_edit_form_valid(self):
        """ Test that a form is valid
        :return: None
        """
        # assign 2 blocks
        data = data_page_type((1, 2))
        form = PageTypeForm(data=data)
        r = form.is_valid()
        self.assertEqual(r, True)
        self.assertEqual(list(form.cleaned_data['blocks']), list(ContentBlock.objects.all()))
        form.save()
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(len(form.instance.blocks.all()), 2)

        # remove 1 block
        data = data_page_type((1,))
        form = PageTypeForm(data=data, instance=form.instance)
        r = form.is_valid()
        self.assertEqual(r, True)
        form.save()
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(len(form.instance.blocks.all()), 1)

    """ Content blocks """
    def test_admin_content_block_page(self):
        """ Test that content block changelist page renders properly
        :return: None
        """
        response = self.client.get(reverse('admin:ninecms_contentblock_changelist'))
        self.assertContains(response, "content block")
        self.assertContains(
            response,
            '<th scope="col" class="sortable column-name"><a href="?o=1">Name</a></th>',
            html=True
        )
        self.assertContains(
            response,
            '<a href="%s">user-menu</a>' % reverse(
                'admin:ninecms_contentblock_change',
                args=(self.block_user_menu.pk,)),
            html=True
        )
        self.assertContains(
            response,
            '<a href="%s">login</a>' % reverse(
                'admin:ninecms_contentblock_change',
                args=(self.block_login.pk,)),
            html=True
        )
        self.assertContains(
            response,
            '<th scope="col"  class="column-page_types_list"><span>Page types</span></th>',
            html=True
        )
        self.assertContains(
            response,
            '<a href="%s">Front Page</a>' % reverse('admin:ninecms_pagetype_change', args=(self.node_rev_front.pk,)),
            html=True
        )

    """ Menus """
    def test_admin_menu_item_add_page(self):
        """ Test that menu item add page renders properly
        :return: None
        """
        response = self.client.get(reverse('admin:ninecms_menuitem_add'))
        self.assertContains(response, '<label for="id_parent">')
        self.assertContains(response, '<label class="required" for="id_weight">')
        self.assertContains(response, '<label for="id_language">')
        self.assertContains(response, '<label for="id_path">')

    """ Logout """
    def test_logout_view(self):
        """ Test that logout form renders properly
        :return: None
        """
        response = assert_front(self, reverse('ninecms:index'))
        self.assertNotContains(response, '<form action="' + reverse('ninecms:login') + '" method="post">')
        self.assertNotContains(response, '<li><a href="#">Login</a></li>')
        self.assertContains(response, '<form action="' + reverse('ninecms:logout') + '" method="post">')

    def test_logout_form_post_valid(self):
        """ Test posting valid data
        :return: None
        """
        data = data_login()
        response = self.client.post(reverse('ninecms:logout'), data, follow=True)
        self.assertContains(response, get_front_title() + '</h1>')
        self.assertContains(response, "Logout successful")
        self.assertRedirects(response, reverse(data['redirect']))

    """ Permissions """
    def test_content_type_perms_view(self):
        """ Test that view renders properly /admin/ninecms/pagetype/<id>/perms
        :return: None
        """
        t_id = self.node_rev_basic.node.page_type_id
        response = self.client.get(reverse('admin:ninecms_pagetype_perms', args=(t_id,)))
        self.assertContains(response, 'Edit permissions for page type')
        self.assertEqual(not response.context['permissions_form'].errors, True)
        self.assertEqual(response.context['page_type'], self.node_rev_basic.node.page_type)

    def test_content_type_perms_view_post_valid(self):
        """ Test posting valid data at /admin/ninecms/pagetype/<id>/perms
        Cannot test for invalid data (simple form)
        Test signal pre_delete for guardian permissions when page type is deleted
        :return: None
        """
        t = PageType(name='other', description="Other type to test perms")
        t.save()
        perms = {'add_node': [self.simple_group.pk], 'change_node': [self.simple_group.pk], 'delete_node': []}

        response = self.client.post(reverse('admin:ninecms_pagetype_perms', args=(t.pk,)), perms, follow=True)
        # set_perms(t, list(ContentTypePermissionsForm().fields.keys()), '_pagetype', perms)
        self.assertContains(response, "Content type &#39;other&#39; has been updated.")
        self.assertRedirects(response, reverse('admin:ninecms_pagetype_changelist'))

        content_type = ContentType.objects.get_for_model(t)
        count = len(GroupObjectPermission.objects.filter(content_type=content_type, object_pk=t.pk))
        self.assertEqual(count, 2)

        t.delete()
        count = len(GroupObjectPermission.objects.filter(content_type=content_type, object_pk=t.pk))
        self.assertEqual(count, 0)

    """ Status page """
    def test_status_page(self):
        """ Test status page
        :return: None
        """
        response = self.client.get(reverse('ninecms:status'))
        self.assertRedirects(response, reverse('admin:index'), status_code=301)

    def test_status_page_post_menu_rebuild(self):
        """ Test status page post menu rebuild
        :return: None
        """
        response = self.client.post(reverse('ninecms:status'), {'menu-rebuild': "Rebuild menu"}, follow=True)
        self.assertRedirects(response, reverse('admin:index'))
        self.assertContains(response, "Menu has been rebuilt.")

    def test_status_page_post_clear_cache(self):
        """ Test status page post clear cache
        :return: None
        """
        response = self.client.post(reverse('ninecms:status'), {'clear-cache': "Clear cache"}, follow=True)
        self.assertRedirects(response, reverse('admin:index'))
        self.assertContains(response, "Cache has been cleared.")
