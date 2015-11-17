# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ninecms', '0003_auto_20150623_1731'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='node',
            options={'permissions': (('access_toolbar', 'Can access the CMS toolbar'), ('use_full_html', 'Can use Full HTML in node body and summary'), ('list_nodes', 'Can list nodes'))},
        ),
    ]
