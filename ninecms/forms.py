""" Form definition for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from ninecms.models import Node, Image, File, Video, ContentBlock, PageType, TaxonomyTerm
from ninecms.utils.sanitize import sanitize, ModelSanitizeForm
from ninecms.utils.manytomany import ManyToManyModelForm, ModelBiMultipleChoiceField


class PageTypeForm(ManyToManyModelForm):
    """ Override default page type form to show related blocks """
    blocks = ModelBiMultipleChoiceField(ContentBlock.objects.all(), double_list="Blocks")

    class Meta:
        """ Meta class """
        model = PageType
        fields = ['name', 'description', 'guidelines', 'url_pattern']


class ContentTypePermissionsForm(forms.Form):
    """ Content type permissions form """
    add_node = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    change_node = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    delete_node = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class ContentNodeEditForm(ManyToManyModelForm):
    """ Node edit or create form """
    terms = ModelBiMultipleChoiceField(TaxonomyTerm.objects.all(), double_list="Terms")

    def __init__(self, *args, **kwargs):
        """ Get user object to check if has full_html permission
        Checks if current_user is already set (eg from ModelAdmin)
        :param args: default arguments
        :param kwargs: default keywords, expecting user
        :return: None
        """
        try:
            self.current_user = kwargs.pop('user', self.current_user)
        except AttributeError:
            self.current_user = kwargs.pop('user', None)
        super(ContentNodeEditForm, self).__init__(*args, **kwargs)

    def clean(self):
        """ Override clean form to bleach
        :return: cleaned data
        """
        cleaned_data = super(ContentNodeEditForm, self).clean()
        full_html = self.current_user and self.current_user.has_perm('ninecms.use_full_html')
        for field in ('title', 'highlight', 'alias'):
            if field in cleaned_data:
                cleaned_data[field] = sanitize(cleaned_data[field], allow_html=False)
        for field in ('summary', 'body'):
            if field in cleaned_data:
                cleaned_data[field] = sanitize(cleaned_data[field], full_html=full_html)
        return cleaned_data

    class Meta:
        """ Form model and fields """
        model = Node
        fields = ['page_type', 'language', 'title', 'user', 'status', 'promote', 'sticky', 'created',
                  'original_translation', 'summary', 'body', 'highlight', 'link', 'weight', 'alias', 'redirect']


class ImageForm(ModelSanitizeForm):
    """ Explicitly define image form in order to sanitize input """
    class Meta:
        """ Form meta """
        model = Image
        fields = ['title', 'group', 'image']
        sanitize = ['title', 'group']

ImageInlineFormset = inlineformset_factory(Node, Image, form=ImageForm, extra=0, min_num=0)


class FileForm(ModelSanitizeForm):
    """ Explicitly define file form in order to sanitize input """
    class Meta:
        """ Form meta """
        model = File
        fields = ['title', 'group', 'file']
        sanitize = ['title', 'group']

FileInlineFormset = inlineformset_factory(Node, File, form=FileForm, extra=0, min_num=0)


class VideoForm(ModelSanitizeForm):
    """ Explicitly define video form in order to sanitize input """
    class Meta:
        """ Form meta """
        model = Video
        fields = ['title', 'group', 'video', 'type', 'media']
        sanitize = ['title', 'group', 'type', 'media']

VideoInlineFormset = inlineformset_factory(Node, Video, form=VideoForm, extra=0, min_num=0)


class RedirectForm(forms.Form):
    """ General purpose form with a hidden redirect field, used in contact form, login form and as a logout form """
    attr = {'class': 'form-control'}
    redirect = forms.CharField(widget=forms.HiddenInput())


class ContactForm(RedirectForm):
    """ Contact form """
    sender_name = forms.CharField(
        max_length=100,
        label=_("Your name"),
        widget=forms.TextInput(attrs=RedirectForm.attr)
    )
    sender_email = forms.EmailField(
        max_length=100,
        label=_("Your email"),
        widget=forms.TextInput(attrs=RedirectForm.attr)
    )
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs=RedirectForm.attr))
    message = forms.CharField(widget=forms.Textarea(attrs=RedirectForm.attr))

    def clean(self):
        """ Additionally to Django clean() (https://docs.djangoproject.com/en/1.7/ref/forms/validation/)
        Sanitize HTML from form data (http://stackoverflow.com/questions/5641901/sanitizing-html-in-submitted-form-data)
        Otherwise the template will escape without stripping if not so specified
        :return: cleaned data
        """
        cleaned_data = super(ContactForm, self).clean()
        for field in ('sender_name', 'sender_email', 'message', 'redirect'):
            if field in cleaned_data:
                cleaned_data[field] = sanitize(cleaned_data[field], allow_html=False)
        if 'subject' in cleaned_data:
            cleaned_data['subject'] = "[Website Feedback] " + sanitize(cleaned_data['subject'], allow_html=False)
        return cleaned_data


class LoginForm(RedirectForm):
    """ Login form """
    username = forms.CharField(max_length=255, label=_("Username"), widget=forms.TextInput(attrs=RedirectForm.attr))
    password = forms.CharField(max_length=255, label=_("Password"), widget=forms.PasswordInput(attrs=RedirectForm.attr))


class SearchForm(forms.Form):
    """ Search form """
    q = forms.CharField(max_length=255, label=_("Search"), widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        """ Override clean function to sanitize data
        :return: cleaned data
        """
        cleaned_data = super(forms.Form, self).clean()
        if 'q' in cleaned_data:
            cleaned_data['q'] = sanitize(cleaned_data['q'], allow_html=False)
        return cleaned_data
