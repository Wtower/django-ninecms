# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ninecms', '0005_auto_20150624_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagelayoutelement',
            name='hidden',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='node',
            name='language',
            field=models.CharField(max_length=2, blank=True, choices=[('el', 'Greek')]),
        ),
    ]
