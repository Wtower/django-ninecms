""" https://gist.github.com/Wtower/0b181cc06f816e4feac14e7c0aa2e9d0 """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple


class ModelBiMultipleChoiceField(forms.ModelMultipleChoiceField):
    """ This shows both ends of m2m in admin """
    def __init__(self, queryset, required=False, widget=None, label=None, initial=None, help_text='',
                 double_list=None, *args, **kwargs):
        """ First add a custom ModelMultipleChoiceField
        Specify a `double_list` label in order to use the double list widget
        Field name should be the same with model's m2m field
        https://www.lasolution.be/blog/related-manytomanyfield-django-admin-site.html
        https://github.com/django/django/blob/master/django/contrib/admin/widgets.py#L24
        """
        if double_list:
            widget = FilteredSelectMultiple(double_list, True)
        super(ModelBiMultipleChoiceField, self).__init__(
            queryset, required, widget, label, initial, help_text, *args, **kwargs)


class ManyToManyModelForm(forms.ModelForm):
    """ This is a generic form to use with the ModelBiMultipleChoiceField """
    def __init__(self, *args, **kwargs):
        """ Initialize form
        :param args
        :param kwargs
        :return: None
        """
        super(ManyToManyModelForm, self).__init__(*args, **kwargs)
        # If this is an existing object, load related
        if self.instance.pk:
            # browse through all form fields and pick the ModelBiMultipleChoiceField
            for field_name in self.base_fields:
                field = self.base_fields[field_name]
                if type(field).__name__ == 'ModelBiMultipleChoiceField':
                    # Get instance property dynamically
                    # field should be same name with reverse model (ie. form.blocks vs instance.blocks)
                    self.initial[field_name] = getattr(self.instance, field_name).values_list('pk', flat=True)

        # # Use the following to add an add new block icon
        # from django.db.models import ManyToManyRel
        # from django.contrib import admin
        # rel = ManyToManyRel(ContentBlock, PageType)
        # self.fields['blocks'].widget = RelatedFieldWidgetWrapper(self.fields['blocks'].widget, rel, admin.site)

    def save(self, *args, **kwargs):
        """ Handle saving of related
        :param args
        :param kwargs
        :return: instance
        """
        instance = super(ManyToManyModelForm, self).save(*args, **kwargs)
        if instance.pk:
            # browse through all form fields and pick the ModelBiMultipleChoiceField
            for field_name in self.base_fields:
                field = self.base_fields[field_name]
                if type(field).__name__ == 'ModelBiMultipleChoiceField':
                    # the m2m records, eg if model field is `blocks`, this would be `instance.blocks.all()`
                    recordset = getattr(self.instance, field_name)
                    records = recordset.all()
                    # remove records that have been removed in form
                    for record in records:
                        if record not in self.cleaned_data[field_name]:
                            recordset.remove(record)
                    # add records that have been added in form
                    for record in self.cleaned_data[field_name]:
                        if record not in records:
                            recordset.add(record)
        return instance
