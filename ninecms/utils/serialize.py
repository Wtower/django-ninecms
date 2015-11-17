""" Serializers utility functions """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.core.serializers.base import Serializer as BaseSerializer
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.json import Serializer as JsonSerializer
from django.utils import six
from django.db import ProgrammingError


# noinspection PyAttributeOutsideInit,PyProtectedMember,PyTypeChecker,PyUnresolvedReferences,PyAbstractClass
class ExtBaseSerializer(BaseSerializer):
    """ Abstract serializer base class.
    Serialize a queryset records with fields AND properties AND related objects
    Default serializer not includes the above
    https://docs.djangoproject.com/en/1.8/topics/serialization/#serialization-formats-json
    Usage example: `data = ExtJsonSerializer().serialize(images, fields=['image', 'node.title'], props=[])`
    """
    def serialize(self, queryset, **options):
        """ Serialize a queryset
        :param queryset: the queryset to serialize
        :param options: options keywords
        :return: the serialized object
        """
        self.options = options
        self.stream = options.pop('stream', six.StringIO())
        self.selected_fields = options.pop('fields', None)
        self.selected_props = options.pop('props', None)
        self.use_natural_keys = options.pop('use_natural_keys', False)
        self.use_natural_foreign_keys = options.pop('use_natural_foreign_keys', False)
        self.use_natural_primary_keys = options.pop('use_natural_primary_keys', False)
        self.start_serialization()
        self.first = True
        # for each record (obj)
        for obj in queryset:
            self.start_object(obj)
            concrete_model = obj._meta.concrete_model
            # for each field of object class (not selected_fields)
            for field in concrete_model._meta.local_fields:
                # if serializable
                if field.serialize:
                    # if not a relationship field
                    if field.rel is None:
                        # if no selected fields or if this field is in selected_fields
                        if self.selected_fields is None or field.attname in self.selected_fields:
                            self.handle_field(obj, field)
                    else:
                        # if no selected fields and field name (eg node_id -> node) in selected fields
                        if self.selected_fields is None or field.attname[:-3] in self.selected_fields:
                            self.handle_fk_field(obj, field)
                        else:
                            # GK: if there is a field in selected_fields which starts as `field__` then fetch related
                            related = [s for s in self.selected_fields if s.startswith(field.attname[:-3] + '__')]
                            if bool(related):
                                self.handle_fk_field_related(obj, field, related[0])
            # for each field in many_to_many fields of the object class
            for field in concrete_model._meta.many_to_many:
                if field.serialize:
                    if self.selected_fields is None or field.attname in self.selected_fields:
                        self.handle_m2m_field(obj, field)
            # GK: for each property specified
            if bool(self.selected_props):
                for field in self.selected_props:
                    self.handle_prop(obj, field)
            self.end_object(obj)
            if self.first:
                self.first = False
        self.end_serialization()
        return self.getvalue()

    def handle_fk_field_related(self, obj, field, related):
        """ Handle an object's related field for serialization
        http://stackoverflow.com/questions/9379249/access-django-models-fields-using-a-string-instead-of-dot-syntax
        :param obj: the object (record)
        :param field: the field to handle
        :param related: the related field name which is asked
        :return: the serialized property
        """
        asked_fields = related.split('__')
        value = obj
        for asked_field in asked_fields:
            try:
                # get the field dynamically
                value = value.__dict__[asked_field]
            except KeyError:
                try:
                    # try if the field is a related object, it can be accessed as cached
                    value = value.__dict__['_%s_cache' % asked_field]
                except KeyError as e:
                    raise ProgrammingError(
                        "The related table for field `%s` is not cached. "
                        "Make sure you have used `select_related` in your query." % asked_field) from e
        self._current[field.name] = value

    def handle_prop(self, obj, field):
        """ Handle an object's property for serialization
        :param obj: the object
        :param field: the property name to handle
        :return: the serialized property
        """
        self._current[field] = getattr(obj, field)()


class ExtPythonSerializer(ExtBaseSerializer, PythonSerializer):
    """ Python serializer base class using ExtBaseSerializer """
    pass


class ExtJsonSerializer(ExtPythonSerializer, JsonSerializer):
    """ JSON serializer base class using ExtBaseSerializer """
    pass
