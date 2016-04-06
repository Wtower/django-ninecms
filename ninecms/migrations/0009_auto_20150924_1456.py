# -*- coding: utf-8 -*-
# Custom migration for fixing page type name issue
from __future__ import unicode_literals

# noinspection PyUnresolvedReferences
from django.db import models, migrations
from django.conf import settings
from ninecms.utils.transliterate import transliterate
import os


def transliterate_folder(field):  # pragma: nocover
    """ Utility function to transliterate a path_file_name
    :param field: string with path_file_name
    :return: transliterated path_file_name
    """
    return '/'.join(list(transliterate(folder, True, True) for folder in field.split('/')))


# noinspection PyUnusedLocal
# noinspection PyPep8Naming
def migrate_path_file_name(apps, schema_editor):  # pragma: nocover
    """ Transliterate the directories of all saved files
    Transliterate the corresponding field values
    :param app registry
    :param schema_editor
    :return: None
    """
    basedir = os.path.join(settings.MEDIA_ROOT, 'ninecms')
    for folder in os.listdir(basedir):
        os.rename(os.path.join(basedir, folder), os.path.join(basedir, transliterate(folder, True, True)))

    Image = apps.get_model('ninecms', 'Image')
    for image in Image.objects.all():
        image.image.name = transliterate_folder(image.image.name)
        image.save()

    File = apps.get_model('ninecms', 'File')
    for file in File.objects.all():
        file.file.name = transliterate_folder(file.file.name)
        file.save()

    Video = apps.get_model('ninecms', 'Video')
    for video in Video.objects.all():
        video.video.name = transliterate_folder(video.video.name)
        video.save()


# noinspection PyUnusedLocal
def reverse(apps, schema_editor):  # pragma: nocover
    """
    Reverse the above operation
    Nothing to do here, transliterated folder names remain
    :param apps: app registry
    :param schema_editor
    :return: None
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('ninecms', '0008_auto_20150819_1516'),
    ]

    operations = [
        migrations.RunPython(migrate_path_file_name, reverse),
    ]
