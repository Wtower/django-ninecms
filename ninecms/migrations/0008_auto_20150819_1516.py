# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ninecms', '0007_auto_20150727_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxonomyterm',
            name='description_node',
            field=models.ForeignKey(related_name='term_described', blank=True, to='ninecms.Node', null=True),
        ),
    ]
