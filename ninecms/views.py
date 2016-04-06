""" View handler definitions for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.template import loader
from django.http import Http404
from django.core.mail import mail_managers, BadHeaderError
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from ninecms.utils.render import NodeView
from ninecms.utils.perms import get_perms, set_perms
from ninecms.utils import status
from ninecms.models import Node, PageType, MenuItem
from ninecms.forms import ContactForm, LoginForm, RedirectForm, ContentTypePermissionsForm


class ContentNodeView(NodeView):
    """ Display a node as invoked by its node id from /cms/content/<node_id>
    If an alias exists then issue redirect to allow a single content page per URL
    """
    def get(self, request, **kwargs):
        """ HTML get for /cms/content/<node_id>
        :param request: the request object
        :param kwargs: contains node_id
        :return: response object
        """
        node = get_object_or_404(Node, id=kwargs['node_id'])
        if node.alias:
            return redirect('ninecms:alias', url_alias=(node.alias + '/'), permanent=True)
        if not node.status and not request.user.has_perm('ninecms.view_unpublished'):
            raise PermissionDenied
        return self.render(node, request)


class AliasView(NodeView):
    """ Render content based on Url Alias """
    def get(self, request, **kwargs):
        """ HTML get for /<url_alias>
        :param request: the request object
        :param kwargs: contains url_alias
        :return: response object
        """
        if kwargs['url_alias'][-1] == '/':
            alias = kwargs['url_alias'][:-1]
            if alias == '/':
                return redirect('ninecms:index', permanent=True)  # pragma: no cover
            try:
                node = self.get_node_by_alias(alias, request)
            except IndexError:
                raise Http404
            if not node.status and not request.user.has_perm('ninecms.view_unpublished'):
                raise PermissionDenied
            if node.redirect:
                return redirect(node.get_redirect_path(), permanent=True)
            return self.render(node, request)
        else:
            return redirect('ninecms:alias', url_alias=(kwargs['url_alias'] + '/'), permanent=True)


class IndexView(NodeView):
    """ Render index at root / """
    def get(self, request):
        """ HTML get for /
        :param request: the request object
        :return: response object
        """
        try:
            node = self.get_node_by_alias('/', request)
        except IndexError:
            messages.warning(request, "No front page has been created yet.")
            return redirect('admin:index')
        return self.render(node, request)


class ContactView(View):
    """ Handle contact post request """
    form_class = ContactForm

    def post(self, request):
        """ Handle contact form send
        :param request: the request object
        :return: response object
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            t = loader.get_template('ninecms/mail_contact.txt')
            c = {
                'sender_name': form.cleaned_data['sender_name'],
                'sender_email': form.cleaned_data['sender_email'],
                'message': form.cleaned_data['message'],
            }
            try:
                mail_managers(form.cleaned_data['subject'], t.render(c))
            except BadHeaderError:  # pragma: no cover
                messages.error(request, _("Contact form message has NOT been sent. Invalid header found."))
            else:
                messages.success(request, _("A message has been sent to the site using the contact form."))
            return redirect(form.cleaned_data['redirect'])
        messages.warning(request, _("Contact form message has NOT been sent. Please fill in all contact form fields."))
        request.session['contact_form_post'] = request.POST
        return redirect(form.cleaned_data['redirect'])


class LoginView(View):
    """ Handle login post request """
    form_class = LoginForm

    def post(self, request):
        """ Handle login form send
        :param request: the request object
        :return: response object
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, _("Login successful for %s.") % user.username)
                else:
                    msg = _("The account is disabled. Please use the contact form for more information.")
                    messages.warning(request, msg)
            else:
                msg = _("Unfortunately the username or password are not correct. "
                        "If you have forgotten your password use the link below the form to recover it.")
                messages.warning(request, msg)
        else:
            messages.warning(request, _("Please fill in all login form fields."))
            request.session['login_form_post'] = request.POST
        return redirect(form.cleaned_data['redirect'])


class LogoutView(View):
    """ Handle logout post request """
    form_class = RedirectForm

    def post(self, request):
        """ Handle logout form send
        :param request: the request object
        :return: response object
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            logout(request)
            messages.success(request, _("Logout successful."))
        return redirect(form.cleaned_data['redirect'])


class ContentTypePermsView(View):
    """ Content edit form at /cms/types/<id>/edit """
    permissions_form_class = ContentTypePermissionsForm

    def get(self, request, **kwargs):
        """ HTML get for /cms/types/<node_id>/edit
        :param request: the request object
        :param kwargs: contains node_id
        :return: response object
        """
        page_type = get_object_or_404(PageType, id=kwargs['type_id'])
        perms = get_perms(page_type, list(self.permissions_form_class().fields.keys()), '_pagetype')
        permissions_form = self.permissions_form_class(initial=perms)
        groups = Group.objects.all().count()
        return render(request, 'admin/ninecms/pagetype/perms_form.html', {
            'permissions_form': permissions_form,
            'groups': groups,
            'page_type': page_type,
            'clone': kwargs.get('clone', False),
        })

    def post(self, request, **kwargs):
        """ HTML post for /cms/types/<id>/edit
        :param request: the request object
        :param kwargs: contains node_id
        :return: response object
        """
        page_type = get_object_or_404(PageType, id=kwargs['type_id'])
        permissions_form = self.permissions_form_class(request.POST)
        groups = Group.objects.all().count()
        if permissions_form.is_valid():
            if request.user.has_perm(('guardian.add_groupobjectpermission',
                                      'guardian.change_groupobjectpermission',
                                      'guardian.delete_groupobjectpermission')):
                set_perms(page_type, list(permissions_form.fields.keys()), '_pagetype', permissions_form.cleaned_data)
            messages.success(request, _("Content type '%s' has been updated.") % page_type.name)
            return redirect('admin:ninecms_pagetype_changelist')
        else:  # pragma: nocover
            messages.warning(request, _("Content type has not been updated. Please check the form for errors."))
            return render(request, 'admin/ninecms/pagetype/perms_form.html', {
                'permissions_form': permissions_form,
                'groups': groups,
                'page_type': page_type,
            })


class StatusView(View):
    """ Status page at cms/status """
    # noinspection PyUnusedLocal
    def get(self, request):
        """ HTML get for status page
        :return: response object
        """
        return redirect('admin:index', permanent=True)

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        """ HTML post for status page
        If menu-rebuild has been posted, rebuild menu and redirect
        If clear-cache has been posted, clear cache and redirect
        :param request: the request object
        :return: response object (redirect to get)
        """
        if 'menu-rebuild' in request.POST:
            # noinspection PyUnresolvedReferences
            MenuItem.objects.rebuild()
            messages.success(request, _("Menu has been rebuilt."))
        if 'clear-cache' in request.POST:
            status.cache_clear()
            messages.success(request, _("Cache has been cleared."))
        return redirect('admin:index')
