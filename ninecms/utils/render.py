""" Node render utility functions """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.conf import settings
from django.views.generic import View
from django.template import loader
from django.db.models import Q
from ninecms.models import Node, PageLayoutElement
from ninecms.signals import block_signal
from ninecms.forms import ContactForm, LoginForm, SearchForm


# noinspection PyMethodMayBeStatic
class NodeView(View):
    """ Basic page render functions
    Base class for ContentNodeEditView, AliasView, IndexView
    """
    def get_node_by_alias(self, alias, request):
        """ Get a node given a path alias
        Query from the opposite direction: https://docs.djangoproject.com/en/1.7/topics/db/examples/many_to_one/
        The order -language returns first objects with language not empty and then with language empty (tested utf8)
        Prefetch related terms is not necessary if node.terms.all are not called in template (adds 1 query)
        But if terms are populated in template then this reduces the number of queries to 1 from 2
        Also .prefetch_related('terms__nodes')\ can be added if necessary
        Requires url alias in db without slashes
        :param alias: a url path alias
        :param request: the request object
        :return: a Node object
        """
        # .prefetch_related('image_set')\
        # .prefetch_related('terms')\
        return Node.objects\
            .filter(alias=alias)\
            .filter(language__in=(request.LANGUAGE_CODE, ''))\
            .select_related('page_type')\
            .order_by('-language', 'id')[0]

    def construct_classes(self, page_name, request):
        """ Construct default body classes for a page
        :param page_name: an individual page type name
        :param request: the request object
        :return: a classes string
        """
        classes = ' '.join(list('page-' + i.replace(' ', '-') for i in page_name))
        classes += ' i18n-' + request.LANGUAGE_CODE
        if request.user.is_authenticated():
            classes += ' logged-in'
        if request.user.is_superuser:
            classes += ' superuser'
        if request.user.has_perm('ninecms.access_toolbar'):
            classes += ' toolbar'
        return classes

    def session_pop(self, request, key, default):
        """ Return the value of a session key if exists and pop it; otherwise return default
        :param request: request object
        :param key: the session key to pop if exists
        :param default: a default value if key not exists
        :return: session key or default value
        """
        return request.session.pop(key) if key in request.session else default

    def block_render(self, template, region, specific, request, context_name, context_value, block_classes=''):
        """ Render a block given a specific template
        Template name priorities: template_region_specific, template_specific, template_region, template
        :param template: block template
        :param region: the region of the block in order to provide specific template, if any
        :param specific: the id of the specific content in order to provide specific template, if any
        :param request: request object
        :param context_name: the name of the context
        :param context_value: the value for the context name
        :return: rendered block string for page render
        """
        region = str(region).replace(' ', '_')
        specific = str(specific).replace(' ', '_')
        t = loader.select_template((
            'ninecms/' + '_'.join(filter(None, (template, region, specific))) + '.html',
            'ninecms/' + '_'.join(filter(None, (template, specific))) + '.html',
            'ninecms/' + '_'.join(filter(None, (template, region))) + '.html',
            'ninecms/' + template + '.html',
        ))
        return t.render({context_name: context_value, 'classes': block_classes}, request)

    def page_render(self, node, request):
        """ Construct the page context
        Render all blocks in a node page
        :param node: the node requested
        :param request: the request object
        :return: rendered page string for context
        """
        # construct the page context
        title = node.title if node.title == settings.SITE_NAME else ' | '.join((node.title, settings.SITE_NAME))
        status = "published" if node.status else "unpublished"
        page = {
            'title': title,
            'classes': self.construct_classes((node.page_type.name, 'content', status), request),
            'node': node,
            'content': self.block_render('block_content', node.page_type.name, node.id, request, 'node', node),
            'author': settings.SITE_AUTHOR,
            'keywords': settings.SITE_KEYWORDS,
        }

        # get all elements (block instances) for this page type and append to page context
        elements = PageLayoutElement.objects\
            .select_related('block')\
            .select_related('block__node')\
            .select_related('block__menu_item')\
            .prefetch_related('block__node__image_set')\
            .filter(page_type=node.page_type_id)\
            .filter(hidden=False)\
            .order_by('region', 'weight', 'id')
        for element in elements:
            # if this region is not in the rendered page then add an empty string
            reg = element.region
            classes = element.block.classes
            if reg not in page:
                page[reg] = ''
            # static node render
            if element.block.type == 'static':
                static_node = element.block.node
                if static_node.language in (request.LANGUAGE_CODE, '') and static_node.status == 1:
                    template = static_node.get_alias_template()
                    page[reg] += self.block_render('block_static', reg, template, request, 'node', static_node, classes)
            # menu render
            elif element.block.type == 'menu':
                menu = element.block.menu_item
                if menu.language in (request.LANGUAGE_CODE, '') and menu.disabled == 0:
                    descendants = menu.get_descendants()
                    page[reg] += self.block_render('block_menu', reg, menu.id, request, 'menu', descendants, classes)
            # signal (view) render
            elif element.block.type == 'signal':
                signal = element.block.signal
                responses = block_signal.send(sender=self.__class__, view=signal, request=request)
                responses = list(filter(lambda response: response[1] is not None, responses))
                if responses:
                    resp = responses[-1][1]
                    page[reg] += self.block_render('block_signal', reg, signal, request, 'content', resp, classes)
            # contact form render
            elif element.block.type == 'contact':
                form = ContactForm(self.session_pop(request, 'contact_form_post', None), initial=request.GET)
                page[reg] += self.block_render('block_contact', reg, None, request, 'form', form, classes)
            # language menu render
            elif element.block.type == 'language':
                labels = settings.LANGUAGE_MENU_LABELS
                page[reg] += self.block_render('block_language', reg, None, request, 'labels', labels, classes)
            # login
            elif element.block.type == 'login':
                form = LoginForm(self.session_pop(request, 'login_form_post', None))
                page[reg] += self.block_render('block_login', reg, None, request, 'form', form, classes)
            # user menu
            elif element.block.type == 'user-menu':
                page[reg] += self.block_render('block_user_menu', reg, None, request, 'user-menu', None, classes)
            # search form
            elif element.block.type == 'search':
                form = SearchForm(request.GET)
                page[reg] += self.block_render('block_search', reg, None, request, 'form', form, classes)
            # search results
            elif element.block.type == 'search-results':
                form = SearchForm(request.GET)
                form.is_valid()
                results = None
                if 'q' in form.cleaned_data:
                    q = form.cleaned_data['q']
                    results = Node.objects.filter(Q(title__icontains=q) | Q(body__icontains=q) |
                                                  Q(summary__icontains=q) | Q(highlight__icontains=q))
                    results = {'q': q, 'nodes': results}
                page[reg] += self.block_render('block_search_results', reg, None, request, 'results', results, classes)
        return page
