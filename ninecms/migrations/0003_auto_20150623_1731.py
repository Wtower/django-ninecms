# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ninecms', '0002_auto_20150519_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='language',
            field=models.CharField(max_length=2, choices=[('el', 'Greek'), ('en', 'English')], blank=True),
        ),
    ]
