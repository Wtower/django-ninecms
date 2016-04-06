"""
Tests declaration for Nine CMS

All tests assume settings.LANGUAGE_CODE is defined

Test files index:
- tests_no_content: Tests with no content, 1 language, anonymous
- tests_content: Tests with content, 1 language, anonymous
- tests_content_i18n: Tests with content, i18n, anonymous
- tests_content_login: Tests with content, 1 language, superuser logged in
- tests_content_login_simple: Tests with content, 1 language, editor logged in

"""
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone, translation
from django.conf import settings
from subprocess import call, check_output
import os
from ninecms.models import PageType, Node, NodeRevision, MenuItem, ContentBlock, Image, \
    TaxonomyTerm, File, Video, validate_file_ext, validate_video_ext

""" Global setup functions """
""" Node System """


def create_user():
    """ Create a default super user
    :return: user object
    """
    try:
        admin = User.objects.get(username='admin')
    except User.DoesNotExist:
        admin = User.objects.create_superuser('admin', 'web@9-dev.com', '1234')
    return admin


def create_simple_user():
    """ Create a default user
    :return: user object
    """
    try:
        user = User.objects.get(username='editor')
    except User.DoesNotExist:
        user = User.objects.create_user('editor', 'web@9-dev.com', '1234')
        user.is_staff = True
        user.save()
    return user


def create_page(page_type_name, page_type_description, alias, language, title):
    """ Create a page
    Create also a node revision for test reasons
    :param page_type_name: the name for the page type
    :param page_type_description: the description for the page type
    :param alias: the node page alias
    :param language: node language
    :param title: node title
    :return: a node revision object from which to obtain node
    """
    # set to default language anyway for coming calls to reverse() to work
    translation.activate(settings.LANGUAGE_CODE)
    admin = create_user()
    page_type, created = PageType.objects.get_or_create(name=page_type_name, description=page_type_description)
    node, created = Node.objects.get_or_create(page_type=page_type, language=language, title=title, user=admin,
                                               body=title + " page.", alias=alias, status=True)
    node_revision, created = NodeRevision.objects.get_or_create(node=node, user=admin, title=title)
    return node_revision


def get_front_title(language=settings.LANGUAGE_CODE, title=""):
    """ Get a localized title for a front page
    :param language: the language for which to get the title
    :param title: a default title, if none provided then return an appropriate for the language
    :return: a localized front page title
    """
    if not title:  # pragma: nocover
        if language == '':
            language = settings.LANGUAGE_CODE
        if language == 'en':
            title = "Software"
        elif language == 'el':
            title = "Logismiko"
    return title


def create_front(alias, language='', title=""):
    """ Create a page for front page
    :param alias: the node page alias
    :param language: node language
    :param title: node title
    :return: a node revision object from which to obtain node
    """
    return create_page('front', 'Front Page', alias, language, get_front_title(language, title))


def assert_no_front(test_case):
    """ Default assertions for no front page
    :param test_case: the test object
    :return: None
    """
    translation.activate(settings.LANGUAGE_CODE)
    response = test_case.client.get(reverse('ninecms:index'), follow=True)
    test_case.assertRedirects(response, '/admin/login/?next=/admin/')


def assert_front(test_case, path, language=settings.LANGUAGE_CODE, title=""):
    """ Default assertions for front page
    :param test_case: the test object
    :param path: the path to test
    :param title: the expected title
    :return: the response object
    """
    translation.activate(language)
    response = test_case.client.get(path, follow=True)
    test_case.assertContains(response, '<title>')
    test_case.assertContains(response, get_front_title(language, title) + '</h1>')
    return response


def get_basic_title(language, title):
    """ Get a localized title for a basic page
    :param language: the language for which to get the title
    :param title: a default title, if none provided then return an appropriate for the language
    :return: a localized title
    """
    if not title:  # pragma: nocover
        if language == '':
            language = settings.LANGUAGE_CODE
        if language == 'en':
            title = "About"
        elif language == 'el':
            title = "Sxetika"
    return title


def create_basic(alias, language='', title=""):
    """ Create a basic page
    :param alias: the node page alias
    :param language: node language
    :param title: node title
    :return: a node revision object from which to obtain node
    """
    return create_page('basic', 'Basic Page', alias, language, get_basic_title(language, title))


def assert_basic(test_case, arg, view='alias', language=settings.LANGUAGE_CODE, title=""):
    """ Default assertions for basic page
    :param test_case: the test object
    :param arg: arguments to view
    :param view: the view to test, default is alias
    :param title: the expected title
    :return: the response object
    """
    translation.activate(language)
    response = test_case.client.get(reverse('ninecms:' + view, args=(arg,)), follow=True)
    test_case.assertContains(response, get_basic_title(language, title) + '</h1>')
    return response


def get_second_language():  # pragma: nocover
    """ Get the second language from the default as defined in settings
    @see http://stackoverflow.com/questions/19502378/python-find-first-instance-of-non-zero-number-in-list
    :return: language code
    """
    if settings.I18N_URLS:
        return next((val for i, val in enumerate(settings.LANGUAGES) if settings.LANGUAGE_CODE not in val), ('', ''))[0]
    else:
        return settings.LANGUAGE_CODE


def data_node(page_type_id, user):
    """ Default form data for a node
    :param page_type_id: the id of the page type of the node
    :param user: the user that edits the node
    :return: a dictionary with the form values
    """
    return {
        'page_type': page_type_id,
        'title': "RC issues",
        'body': '<div>&nbsp;</div><script>alert("This is a test.");</script>',
        'user': user.pk,
        # provide some defaults as this is not constructed from instance
        # format timezone otherwise it returns +00:00 as well which is not accepted
        'created': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'weight': 0,
        # provide management formset fields otherwise we get a ValidationError exception in the test
        'image-TOTAL_FORMS': 3,
        'image-INITIAL_FORMS': 0,
        'file-TOTAL_FORMS': 3,
        'file-INITIAL_FORMS': 0,
        'video-TOTAL_FORMS': 3,
        'video-INITIAL_FORMS': 0,
    }


def data_page_type(blocks):
    return {
        'name': 'article',
        'description': "News article",
        'blocks': blocks,
    }

""" Menu System """


def create_menu(language=''):
    """ Create a standard menu tree
    :param language: menu item language
    :return: the menu item model instance
    """
    if language == '' or language == 'en':
        menu, created = MenuItem.objects.get_or_create(parent=None, weight=0, language=language, path='',
                                                       title="Main Menu")
        MenuItem.objects.get_or_create(parent=menu, weight=0, language=language, path='/', title="Front")
        MenuItem.objects.get_or_create(parent=menu, weight=1, language=language, path='about', title="About")
        MenuItem.objects.get_or_create(parent=menu, weight=2, language=language, path='about#team', title="Team")
        MenuItem.objects.get_or_create(parent=menu, weight=3, language=language, path='http://google.com/',
                                       title="Google")
        MenuItem.objects.get_or_create(parent=menu, weight=4, language=language, path='#bookmark', title="A bookmark")
    else:
        menu, created = MenuItem.objects.get_or_create(parent=None, weight=0, language='el', path='',
                                                       title="Kyriws Menu")
        MenuItem.objects.get_or_create(parent=menu, weight=0, language='el', path='/', title="Arxikh")
        MenuItem.objects.get_or_create(parent=menu, weight=1, language='el', path='about', title="Sxetika")
    return menu


def assert_menu(test_case, response, language=settings.LANGUAGE_CODE):
    """ Assert a menu's content
    Mainly used in test_node_view_block_menu_i18n()
    :param test_case: the test case
    :param response: the response object
    :param language: specified language
    :return:
    """
    if language == '':  # pragma: nocover
        language = 'en'
    language = '/' + language
    if not settings.I18N_URLS:  # pragma: nocover
        language = ''
    test_case.assertContains(response, '<a href="%s/">' % language)
    test_case.assertContains(response, '<a href="%s/about/">' % language)

""" Block System """


def create_block_static(page_type, node):
    """ Create a static block
    :param page_type: where this block will be rendered
    :param node: what this block will contain
    :return: the page layout element
    """
    block, created = ContentBlock.objects.get_or_create(name='static-%s' % node.title, type='static', node=node)
    block.page_types.add(page_type)
    return block


def create_block_menu(page_type, menu):
    """ Create a menu block
    :param page_type: where this block will be rendered
    :param menu: what this block will contain
    :return: the page layout element
    """
    block, created = ContentBlock.objects.get_or_create(name='menu-Main Menu', type='menu', menu_item=menu)
    block.page_types.add(page_type)
    return block


def create_block_signal_terms(page_type):
    """ Create a signal block for terms
    :param page_type: where this block will be rendered
    :return: the page layout element
    """
    block, created = ContentBlock.objects.get_or_create(name='signal-terms', type='signal', signal='terms')
    block.page_types.add(page_type)
    return block


def create_block_simple(page_type, block_type):
    """ Create a contact block
    :param page_type: where this block will be rendered
    :return: the page layout element
    """
    block, created = ContentBlock.objects.get_or_create(name=block_type, type=block_type)
    block.page_types.add(page_type)
    return block

""" Media System """


def create_image(file='test_small.png'):
    """ Create a node with an image
    :return: image model instance
    """
    node_revision = create_basic('about')
    path_file_name = 'ninecms/basic/image/' + file
    img, created = Image.objects.get_or_create(node=node_revision.node, image=path_file_name, title="About")
    return img


def create_file(path_file_name='ninecms/basic/file/readme.txt'):
    """ Create a node with a file
    :param path_file_name: the path file name, provide a different to test for extension validation
    :return: file model instance
    """
    node_revision = create_basic('about')
    file, created = File.objects.get_or_create(node=node_revision.node, file=path_file_name, title="About")
    validate_file_ext(file.file)
    return file


def create_video(path_file_name='ninecms/basic/video/video.mp4'):
    """ Create a node with a video
    :param path_file_name: the path file name, provide a different to test for extension validation
    :return: video model instance
    """
    node_revision = create_basic('about')
    video, created = Video.objects.get_or_create(node=node_revision.node, video=path_file_name, title="About")
    validate_video_ext(video.video)
    return video


def assert_image(test_case, response, img, size, style):
    """ Assert image conditions
    :param test_case: the test case object
    :param response: the response object
    :param img: the image to test for in response
    :param style: the image style to test
    :return: None
    """
    image = img.image
    # original url full: /media/ninecms/basic/image/test.png
    url = img.image.url
    # original url without file: /media/ninecms/basic/image
    url_path = '/'.join(url.split('/')[:-1])
    # original path full: ~/ninecms/media/ninecms/basic/image/test.png
    img_path_file_name = str(image.file)
    # original file: test.png
    img_file_name = os.path.basename(img_path_file_name)

    # style url without file: /media/ninecms/basic/image/large
    style_url_path = '/'.join((url_path, style))
    # style url full: /media/ninecms/basic/image/large/test.png
    style_url = '/'.join((style_url_path, img_file_name))
    # style path without file: ~/ninecms/media/ninecms/basic/image/large
    style_path = os.path.join(os.path.dirname(img_path_file_name), style)
    # style path full: ~/ninecms/media/ninecms/basic/image/large/test.png
    style_path_file_name = os.path.join(style_path, img_file_name)

    if bool(response):  # pragma: nocover
        test_case.assertContains(response, '<img src="' + style_url + '">', html=True)
    test_case.assertEqual(str(check_output(['identify', style_path_file_name])).split(' ')[2], size)
    call(['rm', '-rf', style_path])

""" Taxonomy System """


def create_terms(nodes):
    """ Create a standard taxonomy tree
    :param nodes: a list of nodes to be added
    :return: the root taxonomy term instance
    """
    term, created = TaxonomyTerm.objects.get_or_create(parent=None, name="Tags", weight=0)
    child_term, created = TaxonomyTerm.objects.get_or_create(parent=term, name="General", weight=0)
    child_term.nodes = nodes
    child_term.save()
    return term

""" Contact System """


def data_contact():
    """ Default contact form data
    :return: a dictionary with the form values
    """
    return {
        'sender_name': "George",
        'sender_email': "web@9-dev.com",
        'subject': "Contact subject",
        'message': "Contact message",
        'redirect': 'ninecms:index',
    }

""" Permissions """


def data_login():
    """ Default login form data
    :return: a dictionary with the form values
    """
    return {
        'username': "admin",
        'password': "1234",
        'redirect': 'ninecms:index',
    }

""" Utility functions """


def url_with_lang(url):
    """ Get a url with language, if more than 1 language is defined (and less than 86 which are django default)
    :param url: the url to be returned
    :return: the url with language, if applicable
    """
    prefix = ''
    if 1 < len(settings.LANGUAGES) < 80:  # pragma: nocover
        prefix = '/' + settings.LANGUAGE_CODE
    return prefix + url
