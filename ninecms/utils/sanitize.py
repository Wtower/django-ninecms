""" Sanitize text input """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.utils.html import strip_tags
from django import forms
import bleach


def sanitize(t, allow_html=True, full_html=False):
    """ Bleach clean shortcut function based on pre-defined tags, attributes, styles
    NOTE: the allow_html option makes a strip_tag, not bleach, NEVER expose these values with |safe
    This is because bleach and escape turn all <>& to html entities
    :param t: input text
    :return: output text
    """
    if not t:
        return t
    if not allow_html:
        return strip_tags(t)
    allowed_tags = bleach.ALLOWED_TAGS + ['cite', 'dl', 'dt', 'dd', 'p', 'u', 's', 'sub', 'sup', 'img',
                                          'table', 'thead', 'tbody', 'tr', 'td', 'th', 'hr', 'iframe',
                                          'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'br']
    if full_html:
        allowed_tags += ['div']
    allowed_attributes = {
        'a': ['href', 'title', 'name', 'target', 'class'],
        'abbr': ['title'],
        'acronym': ['title'],
        'p': ['style', 'class'],
        'img': ['src', 'alt', 'title', 'class'],
        'iframe': ['src', 'height', 'width', 'class'],
        'table': ['border', 'cellpadding', 'cellspacing'],
        'th': ['scope', 'rowspan', 'colspan', 'class'],
        'td': ['scope', 'rowspan', 'colspan', 'class'],
        'span': ['style', 'class'],
        'div': ['style', 'class'],
    }
    allowed_styles = ['margin-left', 'text-align', 'width', 'page-break-after', 'display', 'float']
    return bleach.clean(t, tags=allowed_tags, attributes=allowed_attributes, styles=allowed_styles)


class ModelSanitizeForm(forms.ModelForm):
    """ A ModelForm that sanitizes specified fields """
    def clean(self):
        """ Override clean function to sanitize data
        :return: cleaned data
        """
        cleaned_data = super(ModelSanitizeForm, self).clean()
        for field in self.Meta.sanitize:
            if field in cleaned_data:
                cleaned_data[field] = sanitize(cleaned_data[field], allow_html=False)
        return cleaned_data
