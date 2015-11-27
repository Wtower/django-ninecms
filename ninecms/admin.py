""" Admin objects declaration for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.core.exceptions import PermissionDenied
from mptt.admin import MPTTModelAdmin
# noinspection PyPackageRequirements
from guardian.shortcuts import get_objects_for_user
from ninecms import models, forms, views


class PageLayoutElementInline(admin.StackedInline):
    """ Page Layout Element stacked inline to be displayed in Page Types """
    model = models.PageLayoutElement
    extra = 0


@admin.register(models.PageType)
class PageTypeAdmin(admin.ModelAdmin):
    """ Get a list of Page Types """
    list_display = ('name', 'description', 'url_pattern', 'operations')
    list_editable = ('description', 'url_pattern')
    search_fields = ['name']
    inlines = [PageLayoutElementInline]

    # noinspection PyMethodMayBeStatic
    def operations(self, obj):
        """ Return a custom column with operations edit, perms
        :param obj: a node object
        :return: column output
        """
        return ' | '.join((
            '<a href="%s">edit</a>' % reverse('admin:ninecms_pagetype_change', args=(obj.id,)),
            '<a href="%s">permissions</a>' % reverse('admin:ninecms_pagetype_perms', args=(obj.id,)),
        ))
    operations.allow_tags = True

    def get_urls(self):
        """ Override urls to add permissions view
        :return: urls list
        """
        urls = [
            url(r'^(?P<type_id>\d+)/perms/$', self.admin_site.admin_view(views.ContentTypePermsView.as_view()),
                name='ninecms_pagetype_perms')
        ]
        return urls + super(PageTypeAdmin, self).get_urls()


class NodeRevisionInline(admin.StackedInline):
    """ Node Revision stacked inline to be displayed in Nodes (NodeAdmin) """
    model = models.NodeRevision
    extra = 0


class ImageInline(admin.StackedInline):
    """ Images inline to be displayed in Nodes (NodeAdmin) """
    model = models.Image
    form = forms.ImageForm
    extra = 0
    template = 'admin/ninecms/image/stacked.html'


class FileInline(admin.StackedInline):
    """ Files inline to be displayed in Nodes (NodeAdmin) """
    model = models.File
    form = forms.FileForm
    extra = 0


class VideoInline(admin.StackedInline):
    """ Videos inline to be displayed in Nodes (NodeAdmin) """
    model = models.Video
    form = forms.VideoForm
    extra = 0


# noinspection PyMethodMayBeStatic
# noinspection PyUnusedLocal
@admin.register(models.Node)
class NodeAdmin(admin.ModelAdmin):
    """ Get a list of Nodes, also use inlines in Node form """
    list_display = ('title', 'page_type', 'language', 'alias', 'user', 'status', 'promote', 'sticky', 'created',
                    'changed', 'original_translation', 'redirect', 'operations')
    list_editable = ('status', 'promote', 'sticky', 'redirect')
    list_filter = ['page_type', 'created', 'changed']
    search_fields = ['title', 'summary', 'body', 'highlight']
    actions = ['node_publish', 'node_unpublish', 'node_promote', 'node_demote', 'node_sticky', 'node_unsticky',
               'node_reset_alias']
    date_hierarchy = 'created'
    form = forms.ContentNodeEditForm
    # fieldsets returned from overridden get_fieldsets method below
    inlines = [ImageInline, FileInline, VideoInline, NodeRevisionInline]
    save_as = True

    def operations(self, obj):
        """ Return a custom column with 9cms operations view, edit
        :param obj: a node object
        :return: column output
        """
        return ' | '.join((
            '<a href="%s" target="_blank">view</a>' % obj.get_absolute_url(),
            '<a href="%s">edit</a>' % reverse('admin:ninecms_node_change', args=(obj.id,)),
        ))
    operations.allow_tags = True

    def node_publish(self, request, queryset):
        """ Mark all selected nodes as published setting status True
        :param request: the request object
        :param queryset: the Node queryset
        :return: None
        """
        r = queryset.update(status=True)
        messages.success(request, "%d nodes successfully updated as published." % r)
    node_publish.short_description = "Mark selected nodes status as published"

    def node_unpublish(self, request, queryset):
        """ Mark all selected nodes as unpublished setting status False
        :param request: the request object
        :param queryset: the Node queryset
        :return: None
        """
        r = queryset.update(status=False)
        messages.success(request, "%d nodes successfully updated as not published." % r)
    node_unpublish.short_description = "Mark selected nodes status as not published"

    def node_promote(self, request, queryset):
        """ Mark all selected nodes as promoted setting promote True
        :param request: the request object
        :param queryset: the Node queryset
        :return: None
        """
        r = queryset.update(promote=True)
        messages.success(request, "%d nodes successfully updated as promoted." % r)
    node_promote.short_description = "Mark selected nodes as promoted"

    def node_demote(self, request, queryset):
        """ Mark all selected nodes as not promoted setting promote False
        :param request: the request object
        :param queryset: the Node queryset
        :return: None
        """
        r = queryset.update(promote=False)
        messages.success(request, "%d nodes successfully updated as not promoted." % r)
    node_demote.short_description = "Mark selected nodes as not promoted"

    def node_sticky(self, request, queryset):
        """ Mark all selected nodes as sticky setting True
        :param request: the request object
        :param queryset: the Node queryset
        :return: None
        """
        r = queryset.update(sticky=True)
        messages.success(request, "%d nodes successfully updated as sticky." % r)
    node_sticky.short_description = "Mark selected nodes as sticky"

    def node_unsticky(self, request, queryset):
        """ Mark all selected nodes as not sticky setting False
        :param request: the request object
        :param queryset: the Node queryset
        :return: None
        """
        r = queryset.update(sticky=False)
        messages.success(request, "%d nodes successfully updated as not sticky." % r)
    node_unsticky.short_description = "Mark selected nodes as not sticky"

    def node_reset_alias(self, request, queryset):
        """ Reset url alias for all selected nodes
        :param request: the request object
        :param queryset: the Node queryset
        :return: None
        """
        for node in queryset:
            node.alias = ''
            node.save()
        messages.success(request, "%d nodes successfully updated." % len(queryset))
    node_reset_alias.short_description = "Reset url alias for all selected nodes"

    def check_perm(self, request, obj, perm):
        """ Check if a user has permission on the Node
        :param request: the request object
        :param obj: the Node object, if any
        :param perm: the permission to check: has meaning for values 'change', 'delete'
        :return: bool
        """
        if not obj:
            return request.user.has_perm('ninecms.%s_node' % perm)
        types = get_objects_for_user(request.user, 'ninecms.%s_node_pagetype' % perm, klass=models.PageType)
        return obj.page_type in types

    def has_change_permission(self, request, obj=None):
        """ Check user permission on Node change
        :param request: the request object
        :param obj: the Node object
        :return: bool
        """
        return self.check_perm(request, obj, 'change')

    def has_delete_permission(self, request, obj=None):
        """ Check user permission on Node delete
        :param request: the request object
        :param obj: the Node object
        :return: bool
        """
        return self.check_perm(request, obj, 'delete')

    def get_actions(self, request):
        """ Override actions list to check for perms
        If the user sees the actions, then he sees the list, so he already has the change perm
        :param request: the request object
        :return: actions list
        """
        actions = super(NodeAdmin, self).get_actions(request)
        if not request.user.has_perm('ninecms.delete_node') and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        """ Return only objects on which user has permission
        :param request: the request object
        :return: Node queryset
        """
        qs = super(NodeAdmin, self).get_queryset(request)
        types = get_objects_for_user(request.user, 'ninecms.change_node_pagetype', klass=models.PageType)
        return qs.filter(page_type__id__in=types.values_list('id'))

    def get_form(self, request, obj=None, **kwargs):
        form = super(NodeAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                ("Node", {'fields': ('page_type', 'language', 'alias', 'title')}),
                ("Body", {'fields': ('highlight', 'summary', 'body', 'link')}),
                ("Node management", {'fields': ('status', 'promote', 'sticky', 'redirect', 'user',
                                                'created', 'original_translation', 'weight')}),
            )
        else:
            return (
                ("Node", {'fields': ('page_type', 'language', 'title')}),
                ("Body", {'fields': ('highlight', 'summary', 'body', 'link')}),
                ("Node management", {'fields': ('status', 'promote', 'sticky',
                                                'created', 'original_translation', 'weight')}),
            )

    def get_changeform_initial_data(self, request):
        """ Set initial values
        :param request: the request object
        :return: a dictionary with initial values
        """
        return {'user': request.user, 'promote': False, 'sticky': False, 'redirect': False}

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """ Override queryset of page types field to respect permissions
        :param db_field: the database field name
        :param request: the request object
        :param kwargs: keyword arguments such as the queryset
        :return: parent method return
        """
        if db_field.name == 'page_type':
            page_types = get_objects_for_user(request.user, 'ninecms.add_node_pagetype', klass=models.PageType)
            if len(page_types) < 1 and not request.user.is_superuser:
                raise PermissionDenied
            kwargs['queryset'] = page_types
        return super(NodeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.MenuItem)
class MenuItemAdmin(MPTTModelAdmin):
    """ Get a list of Menu Items """
    list_display = ('title', 'language', 'path', 'disabled', 'weight')
    search_fields = ['path', 'title']


# noinspection PyMethodMayBeStatic
@admin.register(models.ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    """ Get a list of blocks """
    list_display = ('description', 'type', 'node', 'menu_item', 'signal', 'elements')
    list_filter = ['type']

    def description(self, obj):
        """ Return a custom column with the block's description
        :param obj: a block object
        :return: column output
        """
        return str(obj)

    def elements(self, obj):
        """ Return a custom column with page types in which each block is an element
        :param obj: a block object
        :return: column output
        """
        r = []
        for element in obj.pagelayoutelement_set.all():
            r.append('<a href="/admin/ninecms/pagelayoutelement/%d">%s</a>' % (element.id, element.page_type))
        return ', '.join(r)
    elements.allow_tags = True
    elements.short_description = "Page types"


@admin.register(models.TaxonomyTerm)
class TaxonomyTermAdmin(MPTTModelAdmin):
    """ Get a list of Taxonomy Terms """
    list_display = ('name', 'description_node', 'weight')

admin.site.site_header = "9cms administration"
admin.site.site_title = "9cms"
admin.site.index_template = 'admin/ninecms/index.html'
