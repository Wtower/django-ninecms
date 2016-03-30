""" Signal definitions for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django import dispatch
from django.db.models.signals import pre_delete
from django.contrib.contenttypes.models import ContentType
# noinspection PyPackageRequirements
from guardian.models import GroupObjectPermission
from ninecms.models import TaxonomyTerm, Node, PageType, Video, Image, File
from ninecms.utils.media import delete_all


# noinspection PyUnusedLocal
@dispatch.receiver(pre_delete)
def pre_delete_tasks(sender, instance, **kwargs):
    """ Delete all relevant permissions from guardian as there is no foreign key to the object
    http://django-guardian.readthedocs.org/en/stable/userguide/caveats.html
    Delete the respective file when an image, a video or a file record is to be deleted
    :param sender: the model to be deleted
    :param instance: the page type object to be deleted
    :param kwargs: other arguments
    :return: None
    """
    if sender == PageType:
        content_type = ContentType.objects.get_for_model(instance)
        GroupObjectPermission.objects.filter(content_type=content_type, object_pk=instance.pk).delete()
    elif sender == Image:
        delete_all(instance.image.path)
    elif sender == Video:
        delete_all(instance.video.path)
    elif sender == File:
        delete_all(instance.file.path)


block_signal = dispatch.Signal(providing_args=['view', 'request'])


@dispatch.receiver(block_signal)
def render_view(**kwargs):
    """ Example of custom views
    :param kwargs: 'view' contains the CMS view to render
    :return: None
    """
    if kwargs['view'] == 'terms':
        return TaxonomyTerm.objects.all()
