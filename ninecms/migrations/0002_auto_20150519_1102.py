# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ninecms', '0001_squashed_0024_auto_20150416_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='taxonomyterm',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
