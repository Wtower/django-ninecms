""" Module definition for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from ninecms.utils.nodes import get_full_path
from ninecms.utils.media import image_path_file_name, file_path_file_name, validate_file_ext, video_path_file_name, \
    validate_video_ext
from ninecms.utils.transliterate import transliterate
import re

"""
Node System
"""


class PageType(models.Model):
    """ Page Type Model: acts as a single page layout """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Specify a unique page type name. A machine name is recommended if to be used in code.",
    )
    description = models.CharField(
        max_length=255,
        help_text="Describe the page type.",
    )
    guidelines = models.CharField(
        max_length=255,
        blank=True,
        help_text="Provide content submission guidelines for this page type.",
    )
    template = models.CharField(
        max_length=255,
        blank=True,
        help_text="Custom template name (deprecated).",
    )
    url_pattern = models.CharField(
        max_length=255,
        blank=True,
        help_text=('Default pattern for page type, if no alias is specified in node edit. '
                   '<a href="https://github.com/Wtower/django-ninecms#url-aliases" target="_blank">More info</a>.'),
    )

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return self.description

    class Meta:
        """ Model meta """
        ordering = ['id']
        # object-specific guardian permissions
        permissions = (
            ('add_node_pagetype', "Add node of a specific page type"),
            ('change_node_pagetype', "Change node of a specific page type"),
            ('delete_node_pagetype', "Delete node of a specific page type"),
        )


class Node(models.Model):
    """ Node Model: basic content record """
    page_type = models.ForeignKey(PageType)
    language = models.CharField(max_length=2, blank=True, choices=settings.LANGUAGES)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    status = models.BooleanField(default=1)
    promote = models.BooleanField(default=0)
    sticky = models.BooleanField(default=0)
    created = models.DateTimeField(default=timezone.now)
    changed = models.DateTimeField(auto_now=True)
    original_translation = models.ForeignKey('self', null=True, blank=True, related_name="Translations")
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    highlight = models.CharField(max_length=255, blank=True)
    link = models.URLField(max_length=255, blank=True)
    weight = models.IntegerField(default=0)
    alias = models.CharField(max_length=255, blank=True, db_index=True)
    redirect = models.BooleanField(default=0)

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return self.title

    def get_absolute_url(self):
        """ Get the full path for the node
        Consider to prefetch urlalias_set
        first() re-runs query
        :return: a path string
        """
        if self.alias:
            return get_full_path(self.alias, self.language)
        return '/cms/content/%i/' % self.id

    def get_redirect_path(self):
        """ Get the redirect path including language (if any)
        :return: full redirect path string
        """
        return get_full_path(self.link, self.language)

    def get_alias_template(self):
        """ Get a template name suggestion based on alias
        :return: string with template name
        """
        if self.alias:
            return self.alias.replace('/', '_')
        return 'node_%d' % self.id

    def save(self, *args, **kwargs):
        """ Override save method to format alias
        After calling parent save, use update in order to avoid issues with new records that get assigned an id
        Not used signals to avoid recursion issues
        :param args
        :param kwargs
        :return: None
        """
        if not self.alias and self.page_type.url_pattern:
            self.alias = self.page_type.url_pattern\
                .replace('[node:title]', transliterate(self.title, False, True))
            regex = re.compile('\[node:(created|changed):(\w\W\w\W\w)\]')
            dates = regex.search(self.alias)
            if dates:
                date_field = self.created if dates.group(1) == 'created' else self.changed
                date_field = DateFormat(date_field).format(dates.group(2))
                self.alias = self.alias.replace(dates.group(0), date_field)
        super(Node, self).save(*args, **kwargs)
        if self.alias.find('[node:id]') >= 0:
            self.alias = self.alias.replace('[node:id]', str(self.id))
            Node.objects.filter(id=self.id).update(alias=self.alias)
        if self.alias and Node.objects.filter(alias=self.alias).filter(language=self.language).count() > 1:
            self.alias = '%s/%d' % (self.alias, self.id)
            Node.objects.filter(id=self.id).update(alias=self.alias)

    class Meta:
        """ Model meta """
        permissions = (
            ('use_full_html', "Can use Full HTML in node body and summary"),
            ('view_unpublished', "Can view unpublished content"),
        )


class NodeRevision(models.Model):
    """ Node Revision Model: Basic content archive, Drupal style """
    node = models.ForeignKey(Node)
    user = models.ForeignKey(User)
    log_entry = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    status = models.BooleanField(default=1)
    promote = models.BooleanField(default=0)
    sticky = models.BooleanField(default=0)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    highlight = models.CharField(max_length=255, blank=True)
    link = models.URLField(max_length=255, blank=True)

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return self.title

"""
Menu System
"""


class MenuItem(MPTTModel):
    """ Menu Item Model: menu tree item in a single tree, paths can be empty for parents """
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    weight = models.IntegerField(default=0, db_index=True)
    language = models.CharField(max_length=2, blank=True, choices=settings.LANGUAGES)
    path = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return str(self.title)

    def full_path(self):
        """ Get the full path including language (if any) and path
        @see 9cms_menu_full_path.ods
        :return: full path string
        """
        path = self.path
        if path.startswith('http:') or path.startswith('https:'):
            return path
        if path.startswith('#'):
            return path
        bookmark = ''
        bookmark_pos = path.find('#')
        if bookmark_pos > 0:
            bookmark = path[bookmark_pos:]
            path = path[:bookmark_pos]
        return get_full_path(path, self.language, bookmark)

    class MPTTMeta:
        """ Set order when inserting items for mptt """
        order_insertion_by = ['weight']

"""
Block System
"""


class ContentBlock(models.Model):
    """ Content Block Model: basic block instance which can be used in several page layouts """
    BLOCK_TYPES = (
        ('static', "Static: link to node"),
        ('menu', "Menu: render a menu or submenu"),
        ('signal', "Signal: call site-specific custom render"),
        ('language', "Language: switch menu"),
        ('user-menu', "User menu: render a menu with login/register and logout links"),
        ('login', "Login: render login form"),
        ('search', "Search: render search form"),
        ('search-results', "Search: render search results"),
        ('contact', "Contact: render contact form"),
    )
    type = models.CharField(
        max_length=50,
        choices=BLOCK_TYPES,
        default='static',
        help_text="How to render the block.",
    )
    classes = models.CharField(
        max_length=255,
        blank=True,
        help_text="Additional CSS classes to append to block.",
    )
    node = models.ForeignKey(
        Node,
        null=True,
        blank=True,
        help_text="The related node with this block (block type: static only).",
    )
    menu_item = TreeForeignKey(
        MenuItem,
        null=True,
        blank=True,
        help_text="The related parent menu item related (block type: menu only).",
    )
    signal = models.CharField(
        max_length=100,
        blank=True,
        help_text=('The signal name to trigger for a '
                   '<a href="https://github.com/Wtower/django-ninecms#views" target="_blank">custom view</a> '
                   '(block type: signal only).'),
    )

    def __str__(self):
        """ Get title based on block type
        :return: model title
        """
        if self.type == 'static':
            return '-'.join((self.type, str(self.node)))
        elif self.type == 'menu':
            return '-'.join((self.type, str(self.menu_item)))
        elif self.type == 'signal':
            return '-'.join((self.type, str(self.signal)))
        return self.type


class PageLayoutElement(models.Model):
    """ Page Layout Element Model: a set of these records define the layout for each page type """
    page_type = models.ForeignKey(PageType)
    region = models.CharField(
        max_length=50,
        db_index=True,
        help_text=('A hard coded region name that is rendered in template index and also used in '
                   '<a href="https://github.com/Wtower/django-ninecms#theme-suggestions" target="_blank">'
                   'theme suggestions</a>.'),
    )
    block = models.ForeignKey(ContentBlock)
    weight = models.IntegerField(
        default=0,
        db_index=True,
        help_text="Elements with greater number in the same region sink to the bottom of the page.",
    )
    hidden = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return ' '.join((str(self.page_type), self.region))

"""
Media System
"""


class Media(models.Model):
    """ Media Model: abstract model for media, one node-many images relationship """
    node = models.ForeignKey(Node)
    title = models.CharField(max_length=255, blank=True)
    group = models.CharField(max_length=50, blank=True)

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return str(self.node)

    class Meta:
        """ Model meta """
        abstract = True


class Image(Media):
    """ Image Model: the basic image record """
    image = models.ImageField(upload_to=image_path_file_name, max_length=255)


class File(Media):
    """ File Model: a file field """
    file = models.FileField(upload_to=file_path_file_name, max_length=255, validators=[validate_file_ext])


class Video(Media):
    """ Video Model: a video file field """
    video = models.FileField(upload_to=video_path_file_name, max_length=255, validators=[validate_video_ext])
    VIDEO_TYPES = (
        ('mp4', 'video/mp4'),
        ('webm', 'video/webm'),
        ('ogg', 'video/ogg'),
        ('flv', 'video/flv'),  # flv will play as source only, use swf for fallback
        ('swf', 'application/x-shockwave-flash'),
        ('jpg', 'image/jpeg'),
    )
    type = models.CharField(max_length=5, choices=VIDEO_TYPES, null=True, blank=True)
    media = models.CharField(max_length=100, blank=True)

"""
Taxonomy System
"""


class TaxonomyTerm(MPTTModel):
    """ Taxonomy term model: the basic term record, m2m relationship with nodes """
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50)
    weight = models.IntegerField(default=0, db_index=True)
    description_node = models.ForeignKey(Node, null=True, blank=True, related_name='term_described')
    nodes = models.ManyToManyField(Node, blank=True, related_name='terms')

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return str(self.name)

    class MPTTMeta:
        """ Set order when inserting items for mptt """
        order_insertion_by = ['weight']
