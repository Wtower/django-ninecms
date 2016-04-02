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
from django.contrib.auth.models import User
from django.utils import translation
from django.conf import settings
from django.core.exceptions import ValidationError
from ninecms.models import Node, image_path_file_name, file_path_file_name, video_path_file_name, PageType
from ninecms.utils.transliterate import transliterate
from django.utils.dateformat import DateFormat
from ninecms.forms import ContactForm, SearchForm
from ninecms.templatetags import ninecms_extras
from ninecms.tests.setup import create_front, create_basic, create_menu, create_block_static, create_block_menu, \
    create_block_signal_terms, create_block_simple, create_page, create_image, create_file, \
    create_video, create_terms, assert_front, assert_basic, create_user, assert_image, data_contact, get_front_title, \
    data_login, url_with_lang


class ContentTests(TestCase):
    """ Tests with some default initial content, no login """
    @classmethod
    def setUpTestData(cls):
        """ Setup initial data:
        Create front page
        Create basic page
        Create menu
        Create blocks
        Create media
        :return: None
        """
        cls.node_rev_front = create_front('/')
        cls.node_rev_basic = create_basic('about')
        cls.menu = create_menu()
        # block system model tests
        cls.block_static = create_block_static(cls.node_rev_front.node.page_type, cls.node_rev_basic.node)
        cls.block_menu = create_block_menu(cls.node_rev_front.node.page_type, cls.menu)
        cls.block_terms = create_block_signal_terms(cls.node_rev_front.node.page_type)
        cls.block_generic = create_block_simple(cls.node_rev_front.node.page_type, 'generic')
        # block system view tests
        for i in range(1, 5):
            node_revision_basic = create_basic('block/' + str(i), settings.LANGUAGE_CODE, 'About ' + str(i))
            if i == 4:  # disable for last one
                node_revision_basic.node.status = 0
                node_revision_basic.node.save()
            create_block_static(cls.node_rev_front.node.page_type, node_revision_basic.node)
            create_page('video', "Video page", '', '', 'Video ' + str(i))
        create_block_simple(cls.node_rev_front.node.page_type, 'language')
        # Media system
        cls.img = create_image()
        cls.img_big = create_image('test_big.jpg')
        cls.img_big_portrait = create_image('test_big_portrait.jpg')
        cls.file = create_file()
        cls.video = create_video()
        # Taxonomy, Contact
        cls.term = create_terms(())
        cls.block_contact = create_block_simple(cls.node_rev_front.node.page_type, 'contact')
        # Extra model tests
        cls.node_rev_basic_no_alias = create_basic('')
        # login / user menu
        cls.block_login = create_block_simple(cls.node_rev_front.node.page_type, 'login')
        cls.block_user_menu = create_block_simple(cls.node_rev_front.node.page_type, 'user-menu')
        # search
        cls.block_search = create_block_simple(cls.node_rev_front.node.page_type, 'search')
        cls.node_rev_basic_search = create_basic('search')
        cls.block_search_results = create_block_simple(cls.node_rev_basic_search.node.page_type, 'search-results')

    """ Node System """
    def test_node_model_methods(self):
        """ Test model methods such as __unicode__
        :return: None
        """
        self.assertEqual(str(self.node_rev_front.node.page_type), self.node_rev_front.node.page_type.description)
        self.assertEqual(str(self.node_rev_front.node), self.node_rev_front.node.title)
        self.assertEqual(str(self.node_rev_front), self.node_rev_front.title)
        self.assertEqual(self.node_rev_front.node.get_absolute_url(), '/')
        self.assertEqual(self.node_rev_basic.node.get_absolute_url(), '/about/')
        self.assertEqual('/cms/content/' in Node.objects.filter(title="Video 1")[0].get_absolute_url(), True)

    def test_node_util_methods(self):
        """ Test utility methods
        :return: None
        """
        self.assertEqual(transliterate("Ξεσκεπάζω την ψυχοφθόρα βδελυγμία"), 'Xeskepazo-tin-psychofthora-bdelygmia')
        self.assertEqual(transliterate("Τάχιστη αλώπηξ βαφής ψημένη γη, δρασκελίζει υπέρ νωθρού κυνός"),
                         'Tachisti-alopix-bafis-psimeni-gi-draskelizei-yper-nothroy-kynos')
        self.assertEqual(transliterate('Ξεσκεπάζω την ψυχοφθόρα βδελυγμία%.doc', True, True),
                         'xeskepazo_tin_psychofthora_bdelygmia.doc')
        self.assertEqual(ninecms_extras.upper_no_intonation("Σχετικά"), "ΣΧΕΤΙΚΑ")

    def test_node_view_with_front(self):
        """ Test node view for front page
        Test simple
        Test front if /// is asked (TestCase cuts trailing slashes anyway though)
        Test front if /%2f/ is asked
        :return:
        """
        assert_front(self, reverse('ninecms:index'))
        assert_front(self, '///')
        assert_front(self, '/%2f/')

    def test_node_view_with_basic(self):
        """ Test basic node
        Test node view of basic page, slash is missing (expecting redirect)
        Test node view of basic page properly
        :return: None
        """
        response = assert_basic(self, 'about')
        self.assertRedirects(response, url_with_lang('/about/'), status_code=301)
        assert_basic(self, 'about/')

    def test_content_view_with_alias(self):
        """ Test view properly /cms/content/<node_id>
        :return: None
        """
        response = assert_basic(self, self.node_rev_basic.node_id, 'content_node')
        self.assertRedirects(response, url_with_lang('/about/'), status_code=301)

    def test_content_view_alias_redirect(self):
        """ Test view redirect from alias
        :return: None
        """
        Node.objects.get_or_create(page_type=self.node_rev_basic.node.page_type, language=settings.LANGUAGE_CODE,
                                   title='redirect', user=create_user(), alias='redirect', link='/', redirect=True)
        response = assert_front(self, '/redirect/')
        # first redirect is /redirect/ to /en/redirect/, last is to front
        # depending on settings.LANGUAGES, therefore not using assertRedirects
        self.assertEqual('/' in response.redirect_chain[-1][0], True)
        self.assertEqual(response.redirect_chain[-1][1], 301)

    def test_content_view_no_alias_unpublished(self):
        """ Test that an unpublished node without alias gets 403
        :return: None
        """
        self.node_rev_basic_no_alias.node.status = False
        self.node_rev_basic_no_alias.node.save()
        response = self.client.get(reverse('ninecms:content_node', args=(self.node_rev_basic_no_alias.node.id,)))
        self.assertEqual(response.status_code, 403)
        self.node_rev_basic_no_alias.node.status = True
        self.node_rev_basic_no_alias.node.save()

    def test_content_view_alias_unpublished(self):
        """ Test that an unpublished node with alias gets 403
        :return: None
        """
        self.node_rev_basic.node.status = False
        self.node_rev_basic.node.save()
        response = self.client.get(url_with_lang('/about/'))
        self.assertEqual(response.status_code, 403)
        self.node_rev_basic.node.status = True
        self.node_rev_basic.node.save()

    def test_node_aliases(self):
        """ Test node save overridden function that produces aliases
        :return: None
        """
        page_type = PageType.objects.create(name='test_aliases', description="Test aliases",
                                            url_pattern='test/[node:title]/[node:created:Y-m-d]/[node:id]')
        node = Node.objects.create(page_type=page_type, title="Test aliases node", user=self.node_rev_basic.node.user)
        alias = 'test/test-aliases-node/%s/%d' % (DateFormat(node.created).format('Y-m-d'), node.id)
        self.assertEqual(node.alias, alias)

    def test_node_aliases_duplicates(self):
        """ Test node save overridden function that produces aliases for duplicate nodes
        :return: None
        """
        page_type = PageType.objects.create(name='test_aliases_duplicates', description="Test aliases duplicates",
                                            url_pattern='test/[node:title]')
        node = Node.objects.create(page_type=page_type, title="Test aliases node", user=self.node_rev_basic.node.user)
        self.assertEqual(node.alias, 'test/test-aliases-node')
        node = Node.objects.create(page_type=page_type, title="Test aliases node", user=self.node_rev_basic.node.user)
        self.assertEqual(node.alias, 'test/test-aliases-node/%d' % node.id)

    """ Menu System """
    def test_menu_model_methods(self):
        """ Test menu model methods
        :return: None
        """
        self.assertEqual(str(self.menu), "Main Menu")

    """ Block System """
    def test_model_methods_blocks(self):
        """ Test model methods for blocks
        :return: None
        """
        self.assertEqual(str(self.block_static), '-'.join(('static', str(self.node_rev_basic.node.title))))
        self.assertEqual(str(self.block_menu), '-'.join(('menu', str(self.menu))))
        self.assertEqual(str(self.block_terms), 'signal-terms')
        self.assertEqual(str(self.block_generic), 'generic')

    def test_node_view_block_static(self):
        """ Test static block for front view
        :return: None
        """
        response = assert_front(self, reverse('ninecms:index'))
        for i in range(1, 4):
            self.assertContains(response, '<div class="body">About ' + str(i) + ' page.</div>')
        self.assertNotContains(response, '<div class="body">About 4 page.</div>')

    def test_node_view_block_menu(self):
        """ Test menu block for front view
        :return: None
        """
        response = assert_front(self, reverse('ninecms:index'))
        self.assertContains(response, '<a href="/">')
        self.assertContains(response, '<a href="/about/">')
        self.assertContains(response, '<a href="/about/#team">')
        self.assertContains(response, '<a href="http://google.com/">')
        self.assertContains(response, '<a href="#bookmark">')

    def test_node_view_block_menu_root_disabled(self):
        """ Test menu block for front view if root is disabled
        :return: None
        """
        self.menu.disabled = True
        self.menu.save()
        response = assert_front(self, reverse('ninecms:index'))
        self.assertNotContains(response, '<a href="/">Front</a>', html=True)
        self.assertNotContains(response, '<a href="/about/">About</a>', html=True)
        self.menu.disabled = False
        self.menu.save()

    def test_node_view_block_menu_item_disabled(self):
        """ Test menu block for front view if item is disabled
        :return: None
        """
        menu_item_disabled = self.menu.children.last()
        menu_item_disabled.disabled = True
        # saving parent does not save children
        menu_item_disabled.save()
        response = assert_front(self, reverse('ninecms:index'))
        self.assertContains(response, '<a href="/">')
        self.assertNotContains(response, '<a href="/about">')
        menu_item_disabled.disabled = False
        menu_item_disabled.save()

    def test_node_view_block_language(self):
        """ Test block for language menu
        :return: None
        """
        response = assert_front(self, reverse('ninecms:index'))
        self.assertContains(response, '<ul class="nav navbar-nav navbar-right language menu')

    """ Media System """
    def test_image_model_methods(self):
        """ Test image model methods
        :return: None
        """
        self.assertEqual(str(self.img), str(self.img.node))
        self.assertEqual(image_path_file_name(self.img, 'test_small.png'), self.img.image)

    def test_file_model_methods(self):
        """ Test file model methods
        :return: None
        """
        self.assertEqual(str(self.file), str(self.file.node))
        self.assertEqual(file_path_file_name(self.file, 'readme.txt'), self.file.file)
        with self.assertRaises(ValidationError):
            create_file('ninecms/basic/file/readme.php')

    def test_video_model_methods(self):
        """ Test video model methods
        :return: None
        """
        self.assertEqual(str(self.video), str(self.video.node))
        self.assertEqual(video_path_file_name(self.video, 'video.mp4'), self.video.video)
        with self.assertRaises(ValidationError):
            create_video('ninecms/basic/video/video.php')

    def test_image_style_upscale(self):
        """ Test thumbnail-upscale
        :return: None
        """
        ninecms_extras.image_style(self.img.image, 'thumbnail_upscale')
        assert_image(self, None, self.img, '150x150', 'thumbnail_upscale')

    def test_image_style_thumbnail_with_large(self):
        """ Test thumbnail with large image
        :return: None
        """
        ninecms_extras.image_style(self.img_big.image, 'thumbnail')
        assert_image(self, None, self.img_big, '150x73', 'thumbnail')

    def test_image_style_crop_thumbnail(self):
        """ Test crop-thumbnail with large image
        :return: None
        """
        ninecms_extras.image_style(self.img_big.image, 'blog_style')
        assert_image(self, None, self.img_big, '350x226', 'blog_style')

    def test_image_style_crop_thumbnail_portrait(self):
        """ Test crop-thumbnail with large image portrait
        :return: None
        """
        ninecms_extras.image_style(self.img_big_portrait.image, 'blog_style')
        assert_image(self, None, self.img_big_portrait, '350x226', 'blog_style')

    """ Taxonomy System """
    def test_model_methods_terms(self):
        """ Test model methods
        :return: None
        """
        self.assertEqual(str(self.term), self.term.name)

    def test_node_view_terms_signals(self):
        """ Test that terms are rendered properly in block
        Test that signals work properly
        :return: None
        """
        response = assert_front(self, reverse('ninecms:index'))
        expected = '<li>Terms<ul><li>Tags<ul class="children"><li>General</li></ul></li></ul></li>'
        self.assertContains(response, expected, html=True)

    """ Contact System """
    def test_contact_form_invalid(self):
        """ Test that an empty form is invalid
        :return: None
        """
        form = ContactForm()
        self.assertEqual(form.is_valid(), False)

    def test_contact_form_valid(self):
        """ Test that a form is valid
        :return: None
        """
        form = ContactForm(data=data_contact())
        self.assertEqual(form.is_valid(), True)

    def test_contact_view(self):
        """ Test that view renders properly
        :return: None
        """
        response = assert_front(self, reverse('ninecms:index'))
        self.assertContains(response, '<form action="' + reverse('ninecms:contact') + '" method="post"')

    def test_contact_form_post_invalid(self):
        """ Test posting invalid data
        :return: None
        """
        data = data_contact()
        del data['sender_name']
        response = self.client.post(reverse('ninecms:contact'), data, follow=True)
        self.assertContains(response, get_front_title() + '</h1>')
        self.assertContains(response, "Contact form message has NOT been sent. Please fill in all contact form fields.")
        self.assertRedirects(response, reverse(data['redirect']))

    def test_contact_form_post_valid(self):
        """ Test posting valid data
        :return: None
        """
        data = data_contact()
        response = self.client.post(reverse('ninecms:contact'), data, follow=True)
        self.assertContains(response, get_front_title() + '</h1>')
        self.assertContains(response, "A message has been sent to the site using the contact form.")
        self.assertRedirects(response, reverse(data['redirect']))
        # https://docs.djangoproject.com/en/1.8/topics/testing/tools/#email-services
        # doesn't work; probably requires to get the mail object; test externally ok
        # self.assertEqual(len(mail.outbox), 1)

    """ Permissions """
    def test_login_view(self):
        """ Test that login form, user menu render properly
        :return: None
        """
        response = assert_front(self, reverse('ninecms:index'))
        self.assertContains(response, '<form action="' + reverse('ninecms:login') + '" method="post">')
        self.assertContains(response, '<li><a href="#">Login</a></li>')
        self.assertNotContains(response, '<form action="' + reverse('ninecms:logout') + '" method="post">')

    def test_login_form_post_invalid(self):
        """ Test posting invalid data
        :return: None
        """
        data = data_login()
        del data['password']
        response = self.client.post(reverse('ninecms:login'), data, follow=True)
        self.assertContains(response, get_front_title() + '</h1>')
        self.assertContains(response, "Please fill in all login form fields.")
        self.assertRedirects(response, reverse(data['redirect']))

    def test_login_form_post_invalid_wrong_password(self):
        """ Test posting invalid data: wrong password
        :return: None
        """
        data = data_login()
        data['password'] = "wrong"
        response = self.client.post(reverse('ninecms:login'), data, follow=True)
        self.assertContains(response, get_front_title() + '</h1>')
        self.assertContains(response, "Unfortunately the username or password are not correct.")
        self.assertRedirects(response, reverse(data['redirect']))

    def test_login_form_post_invalid_inactive(self):
        """ Test posting invalid data: inactive user
        :return: None
        """
        user = User.objects.get(username="admin")
        user.is_active = False
        user.save()
        data = data_login()
        response = self.client.post(reverse('ninecms:login'), data, follow=True)
        self.assertContains(response, get_front_title() + '</h1>')
        self.assertContains(response, "The account is disabled.")
        self.assertRedirects(response, reverse(data['redirect']))
        user.is_active = True
        user.save()

    def test_login_form_post_valid(self):
        """ Test posting valid data
        :return: None
        """
        data = data_login()
        response = self.client.post(reverse('ninecms:login'), data, follow=True)
        self.assertContains(response, get_front_title() + '</h1>')
        self.assertContains(response, "Login successful for")
        self.assertRedirects(response, reverse(data['redirect']))

    """ Search System """
    def test_search_form_valid(self):
        """ Test that a search form is valid
        :return: None
        """
        form = SearchForm(data={'q': "test"})
        self.assertEqual(form.is_valid(), True)

    def test_search_view(self):
        """ Test that search form renders properly
        :return: None
        """
        response = assert_front(self, reverse('ninecms:index'))
        self.assertContains(response, '<form id="searchform" action="/search/" method="get">')

    def test_search_results_view(self):
        """ Test search results view node
        :return: None
        """
        translation.activate(settings.LANGUAGE_CODE)
        response = self.client.get(reverse('ninecms:alias', args=('search/',)), {'q': 'About'})
        self.assertContains(response, '/block/1/">About 1</a>')
        response = self.client.get(reverse('ninecms:alias', args=('search/',)), {'q': 'test'})
        self.assertContains(response, '<p>No results found.</p>')
