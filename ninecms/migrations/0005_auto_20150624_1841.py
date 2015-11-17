# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ninecms', '0004_auto_20150624_1131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pagetype',
            options={'permissions': (('list_nodes_pagetype', 'List nodes of a specific page type'), ('add_node_pagetype', 'Add node of a specific page type'), ('change_node_pagetype', 'Change node of a specific page type'), ('delete_node_pagetype', 'Delete node of a specific page type')), 'ordering': ['id']},
        ),
    ]
