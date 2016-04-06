""" NineCMS custom template filters and tags """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django import template
from django.template.defaultfilters import stringfilter
from django.template import Context
from ninecms.utils.media import image_style as util_image
from ninecms.utils.transliterate import upper_no_intonation as util_upper
from ninecms.utils.nodes import get_clean_url
from ninecms.utils import status


register = template.Library()


@register.filter
def image_style(image, style):
    """ Return the url of different image style
    :param image: An image url
    :param style: Specify style to return image
    :return: image url of specified style
    """
    return util_image(image, style)


class FieldsetNode(template.Node):  # pragma: nocover
    """ Fieldset renderer for 'fieldset' tag (see below) """
    def __init__(self, nodelist, fieldset_name):
        """ Initialize renderer class
        https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/#writing-the-renderer
        https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/#passing-template-variables-to-the-tag
        :param nodelist: a list of the template nodes inside a block of 'fieldset'
        :param fieldset_name: the name of the fieldset
        :return: None
        """
        self.nodelist = nodelist
        # if not in quotes, get variable from context
        if not (fieldset_name[0] == fieldset_name[-1] and fieldset_name[0] in ('"', "'")):  # pragma: nocover
            self.fieldset_name = template.Variable(fieldset_name)
            self.fieldset_id = fieldset_name
            self.resolve = True
        else:
            self.fieldset_name = fieldset_name[1:-1]
            self.fieldset_id = self.fieldset_name
            self.resolve = False

    def render(self, context):
        """ Render the inside of a fieldset block based on template file
        https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/#auto-escaping-considerations
        :param context: the previous template context
        :return: HTML string
        """
        t = context.template.engine.get_template('ninecms/fieldset.html')
        return t.render(Context({
            'var': self.nodelist.render(context),
            'name': self.fieldset_name.resolve(context) if self.resolve else self.fieldset_name,
            'id': self.fieldset_id,
        }, autoescape=context.autoescape))


@register.tag
def fieldset(parser, token):  # pragma: nocover
    """ Compilation function for fieldset block tag
    Render a form fieldset
    *This is an aux tag that is not used and excluded from coverage tests*
    https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/#writing-the-compilation-function
    https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/#parsing-until-another-block-tag
    http://stackoverflow.com/a/30097784/940098
    :param parser: template parser
    :param token: tag name and variables
    :return: HTML string
    """
    try:
        tag_name, fieldset_name = token.split_contents()
    except ValueError:  # pragma: nocover
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    nodelist = parser.parse(('endfieldset',))
    parser.delete_first_token()
    return FieldsetNode(nodelist, fieldset_name)


@register.inclusion_tag('ninecms/field.html')
def field(field_var):
    """ Render a field based on template
    https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/#inclusion-tags
    Possibly add parameter for custom classes
    :param field_var: the field variable
    :return: the template context
    """
    return {'field': field_var}


@register.filter
def upper_no_intonation(s):
    """ Convert a string to uppercase, removing any intonation
    :param s: the string to convert
    :return: the converted string
    """
    return util_upper(s)


@register.filter
def active_trail(menu, url):
    """ Get the active menu item based on url provided, and all of its ancestors
    To be used to check each individual node's path if in this list so to obtain the active trail
    Also remove language part from url if i18n urls are enabled
    :param menu: the parent menu
    :param url: the current url to check against for the active path (should be request.path)
    :return: a recordset of all active menu ancestors
    """
    return menu.filter(path=get_clean_url(url)).get_ancestors(include_self=True) if menu else []


@register.filter
def flatten(records, fld):
    """ Flatten a recordset to list of a particular field
    :param records: the recordset to flatten
    :param fld: the field from the records to include in list
    :return: a list
    """
    return [path for fields in records.values_list(fld) for path in fields] if records else []


@register.filter
@stringfilter
def strip(string, char):  # pragma: nocover
    """ Strip a specified character from a string
    Helper filter that should exist in Django, not currently used
    :param string:
    :param char:
    :return: stripped string
    """
    return string.strip(char)

@register.filter
def check_path_active(node_path, request_path):
    """ Check that the two paths are equal, ignoring leading or trailing slashes
    Helper function for improving readability
    Mainly used in menu templates
    :param node_path: the menu item path
    :param request_path: the request path
    :return: boolean
    """
    url = get_clean_url(request_path)
    return node_path == url or node_path == url.strip('/')

@register.inclusion_tag('ninecms/glyphicon.html')
def glyphicon(icon):
    """ Shorthand for bootstrap glyphicon markup
    :param icon: the icon to present, gets appended to glyphicon-{{ icon }}
    :return: the template context
    """
    return {'icon': icon}

@register.assignment_tag(takes_context=True)
def get_status(context):
    return {
        'version': status.version(),
        'packages': status.packages(),
        'updates': status.updates(),
        'django_check': status.django_check(),
        'migrations': status.django_migrations(),
        'permissions': status.permissions_status(),
        'imagemagick': status.imagemagick_status(),
        'user_stats': status.user_stat(context['request'].user),
    }
