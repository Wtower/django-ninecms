""" Module definition for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _
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
        verbose_name=_("name"),
        help_text=_("Specify a unique page type name. A machine name is recommended if to be used in code."),
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_("description"),
        help_text=_("Describe the page type."),
    )
    guidelines = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("guidelines"),
        help_text=_("Provide content submission guidelines for this page type."),
    )
    url_pattern = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Default pattern for page type, if no alias is specified in node edit. '
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
            ('add_node_pagetype', _("Add node of a specific page type")),
            ('change_node_pagetype', _("Change node of a specific page type")),
            ('delete_node_pagetype', _("Delete node of a specific page type")),
        )
        verbose_name = _("page type")
        verbose_name_plural = _("page types")


class Node(models.Model):
    """ Node Model: basic content record """
    page_type = models.ForeignKey(PageType, verbose_name=_("page type"))
    language = models.CharField(max_length=2, blank=True, choices=global_settings.LANGUAGES, verbose_name=_("language"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    user = models.ForeignKey(User, verbose_name=_("user"))
    status = models.BooleanField(default=1, verbose_name=_("published"))
    promote = models.BooleanField(default=0, verbose_name=_("promoted"))
    sticky = models.BooleanField(default=0, verbose_name=_("sticky"))
    created = models.DateTimeField(default=timezone.now, verbose_name=_("date created"))
    changed = models.DateTimeField(auto_now=True, verbose_name=_("date changed"))
    original_translation = models.ForeignKey('self', null=True, blank=True, related_name="Translations",
                                             verbose_name=_("original translation"))
    summary = models.TextField(blank=True, verbose_name=_("summary"))
    body = models.TextField(blank=True, verbose_name=_("body"))
    highlight = models.CharField(max_length=255, blank=True, verbose_name=_("highlight"))
    link = models.URLField(max_length=255, blank=True, verbose_name=_("link"))
    weight = models.IntegerField(default=0, verbose_name=_("order weight"))
    alias = models.CharField(max_length=255, blank=True, db_index=True, verbose_name=_("alias"))
    redirect = models.BooleanField(default=0, verbose_name=_("redirect"))

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
            ('use_full_html', _("Can use Full HTML in node body and summary")),
            ('view_unpublished', _("Can view unpublished content")),
        )
        verbose_name = _("node")
        verbose_name_plural = _("nodes")


class NodeRevision(models.Model):
    """ Node Revision Model: Basic content archive, Drupal style """
    node = models.ForeignKey(Node, verbose_name=_("node"))
    user = models.ForeignKey(User, verbose_name=_("user"))
    log_entry = models.CharField(max_length=255, blank=True, verbose_name=_("log entry"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("date created"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    status = models.BooleanField(default=1, verbose_name=_("published"))
    promote = models.BooleanField(default=0, verbose_name=_("promoted"))
    sticky = models.BooleanField(default=0, verbose_name=_("sticky"))
    summary = models.TextField(blank=True, verbose_name=_("summary"))
    body = models.TextField(blank=True, verbose_name=_("body"))
    highlight = models.CharField(max_length=255, blank=True, verbose_name=_("highlight"))
    link = models.URLField(max_length=255, blank=True, verbose_name=_("link"))

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return self.title

    class Meta:
        """ Model meta """
        verbose_name = _("node revision")
        verbose_name_plural = _("node revisions")

"""
Menu System
"""


class MenuItem(MPTTModel):
    """ Menu Item Model: menu tree item in a single tree, paths can be empty for parents """
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_("parent menu"))
    weight = models.IntegerField(default=0, db_index=True, verbose_name=_("order weight"))
    language = models.CharField(max_length=2, blank=True, choices=global_settings.LANGUAGES, verbose_name=_("language"))
    path = models.CharField(max_length=255, blank=True, verbose_name=_("path"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    disabled = models.BooleanField(default=False, verbose_name=_("disabled"))

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

    class Meta:
        """ Model meta """
        verbose_name = _("menu item")
        verbose_name_plural = _("menu items")

"""
Block System
"""


class ContentBlock(models.Model):
    """ Content Block Model: basic block instance which can be used in several page layouts """
    name = models.CharField(
        max_length=100,
        # @todo temp: change null and unique in migrate 14 after having a default
        null=True,
        # unique=True,
        verbose_name=_("name"),
        # @todo run make translate
        help_text=_("Specify a unique block machine name."),
    )
    BLOCK_TYPES = (
        ('static', _("Static: link to node")),
        ('menu', _("Menu: render a menu or submenu")),
        ('signal', _("Signal: call site-specific custom render")),
        ('language', _("Language: switch menu")),
        ('user-menu', _("User menu: render a menu with login/register and logout links")),
        ('login', _("Login: render login form")),
        ('search', _("Search: render search form")),
        ('search-results', _("Search: render search results")),
        ('contact', _("Contact: render contact form")),
    )
    type = models.CharField(
        max_length=50,
        choices=BLOCK_TYPES,
        default='static',
        verbose_name=_("type"),
        help_text=_("How to render the block."),
    )
    classes = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Additional CSS classes to append to block."),
    )
    node = models.ForeignKey(
        Node,
        null=True,
        blank=True,
        verbose_name=_("node"),
        help_text=_("The related node with this block (block type: static only)."),
    )
    menu_item = TreeForeignKey(
        MenuItem,
        null=True,
        blank=True,
        verbose_name=_("menu item"),
        help_text=_("The related parent menu item related (block type: menu only)."),
    )
    signal = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('The signal name to trigger for a '
                    '<a href="https://github.com/Wtower/django-ninecms#views" target="_blank">custom view</a> '
                    '(block type: signal only).'),
    )
    page_types = models.ManyToManyField(
        PageType,
        blank=True,
        related_name='blocks',
        verbose_name=_("page types"),
    )

    def __str__(self):
        """ Get block name
        :return: name
        """
        return self.name

    class Meta:
        """ Model meta """
        verbose_name = _("content block")
        verbose_name_plural = _("content blocks")


# @todo remove model in migration 14
class PageLayoutElement(models.Model):
    """ Page Layout Element Model: a set of these records define the layout for each page type """
    page_type = models.ForeignKey(PageType, verbose_name=_("page type"))
    region = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name=_("region"),
        help_text=_('A hard coded region name that is rendered in template index and also used in '
                    '<a href="https://github.com/Wtower/django-ninecms#theme-suggestions" target="_blank">'
                    'theme suggestions</a>.'),
    )
    block = models.ForeignKey(ContentBlock, verbose_name=_("content block"))
    weight = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name=_("order weight"),
        help_text=_("Elements with greater number in the same region sink to the bottom of the page."),
    )
    hidden = models.BooleanField(default=False, db_index=True, verbose_name=_("hidden"))

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return ' '.join((str(self.page_type), self.region))  # pragma: nocover

    class Meta:
        """ Model meta """
        verbose_name = _("page layout element")
        verbose_name_plural = _("page layout elements")

"""
Media System
"""


class Media(models.Model):
    """ Media Model: abstract model for media, one node-many images relationship """
    node = models.ForeignKey(Node, verbose_name=_("node"))
    title = models.CharField(max_length=255, blank=True, verbose_name=_("title"))
    group = models.CharField(max_length=50, blank=True, verbose_name=_("group"))

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
    image = models.ImageField(upload_to=image_path_file_name, max_length=255, verbose_name=_("image"))

    class Meta:
        """ Model meta """
        verbose_name = _("image")
        verbose_name_plural = _("images")


class File(Media):
    """ File Model: a file field """
    file = models.FileField(upload_to=file_path_file_name, max_length=255, validators=[validate_file_ext],
                            verbose_name=_("file"))

    class Meta:
        """ Model meta """
        verbose_name = _("file")
        verbose_name_plural = _("files")


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
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_("parent term"))
    name = models.CharField(max_length=50, verbose_name=_("name"))
    weight = models.IntegerField(default=0, db_index=True, verbose_name=_("order weight"))
    description_node = models.ForeignKey(Node, null=True, blank=True, related_name='term_described',
                                         verbose_name=_("description node"))
    nodes = models.ManyToManyField(Node, blank=True, related_name='terms', verbose_name=_("nodes"))

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return str(self.name)

    class MPTTMeta:
        """ Set order when inserting items for mptt """
        order_insertion_by = ['weight']

    class Meta:
        """ Model meta """
        verbose_name = _("taxonomy term")
        verbose_name_plural = _("taxonomy terms")
