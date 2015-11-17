# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import datetime
from django.utils.timezone import utc
import ninecms.models
import mptt.fields


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# ninecms.migrations.0022_auto_20150416_1454

# noinspection PySetFunctionToLiteral
class Migration(migrations.Migration):
    replaces = [
        ('ninecms', '0001_initial'),
        ('ninecms', '0002_auto_20150212_1224'),
        ('ninecms', '0003_auto_20150215_1113'),
        ('ninecms', '0004_auto_20150215_1728'),
        ('ninecms', '0005_contentblock_pagelayoutelement'),
        ('ninecms', '0006_auto_20150226_2239'),
        ('ninecms', '0007_auto_20150301_1301'),
        ('ninecms', '0008_auto_20150302_1559'),
        ('ninecms', '0009_auto_20150302_1632'),
        ('ninecms', '0010_auto_20150306_1809'),
        ('ninecms', '0011_auto_20150309_1712'),
        ('ninecms', '0012_auto_20150309_1716'),
        ('ninecms', '0013_auto_20150310_1355'),
        ('ninecms', '0014_file_video'),
        ('ninecms', '0015_auto_20150319_1407'),
        ('ninecms', '0016_auto_20150319_1513'),
        ('ninecms', '0017_auto_20150326_1505'),
        ('ninecms', '0018_auto_20150406_1733'),
        ('ninecms', '0019_auto_20150414_1234'),
        ('ninecms', '0020_auto_20150414_1620'),
        ('ninecms', '0021_auto_20150416_1453'),
        ('ninecms', '0022_auto_20150416_1454'),
        ('ninecms', '0023_auto_20150416_1538'),
        ('ninecms', '0024_auto_20150416_1551')
    ]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                # ('slug', models.SlugField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NodeRevision',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('language', models.CharField(blank=True, max_length=2)),
                ('revision', models.IntegerField(default=1)),
                ('log_entry', models.CharField(blank=True, max_length=255)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=1)),
                ('promote', models.BooleanField(default=0)),
                ('sticky', models.BooleanField(default=0)),
                ('summary', models.TextField(blank=True)),
                ('body', models.TextField(blank=True)),
                ('highlight', models.CharField(blank=True, max_length=255)),
                ('weight', models.IntegerField(default=0)),
                ('node', models.ForeignKey(to='ninecms.Node')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('guidelines', models.CharField(blank=True, max_length=255)),
                ('template', models.CharField(blank=True, max_length=255)),
                ('url_pattern', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='node',
            name='page_type',
            field=models.ForeignKey(to='ninecms.PageType'),
        ),
        migrations.AlterUniqueTogether(
            name='noderevision',
            unique_together=set([('node', 'language', 'revision')]),
        ),
        # migrations.AlterField(
        #     model_name='node',
        #     name='slug',
        #     field=models.CharField(db_index=True, blank=True, max_length=100),
        # ),
        migrations.CreateModel(
            name='ContentBlock',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('type', models.CharField(default=b'static', max_length=50)),
                ('node', models.ForeignKey(to='ninecms.Node')),
            ],
        ),
        migrations.CreateModel(
            name='PageLayoutElement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('region', models.CharField(db_index=True, max_length=50)),
                ('weight', models.IntegerField(db_index=True, default=0)),
                ('block', models.ForeignKey(to='ninecms.ContentBlock')),
                ('page_type', models.ForeignKey(to='ninecms.PageType')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='pagelayoutelement',
            unique_together=set([('page_type', 'block')]),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('image', models.ImageField(upload_to=ninecms.models.image_path_file_name, max_length=255)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('group', models.CharField(blank=True, max_length=50)),
                ('node', models.ForeignKey(to='ninecms.Node')),
            ],
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='type',
            field=models.CharField(default=b'static', max_length=50, choices=[
                (b'static', b'Static: link to node'),
                (b'menu', b'Menu: render a menu or submenu'),
                (b'signal', b'Signal: call site-specific custom render'),
                (b'language', b'Language: switch menu'),
                (b'user-menu', b'User menu: render a menu with login/register and logout links'),
                (b'login', b'Login: render login form'), (b'search', b'Search: render search form')]),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('weight', models.IntegerField(db_index=True, default=0)),
                ('disabled', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='ninecms.MenuItem', null=True, blank=True,
                                                      related_name='children')),
                ('language', models.CharField(blank=True, max_length=2)),
                ('path', models.CharField(blank=True, max_length=255)),
                ('title', models.CharField(default='Default', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contentblock',
            name='menu_item',
            field=mptt.fields.TreeForeignKey(to='ninecms.MenuItem', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='node',
            field=models.ForeignKey(to='ninecms.Node', null=True, blank=True),
        ),
        # migrations.CreateModel(
        #     name='UrlAlias',
        #     fields=[
        #         ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
        #         ('language', models.CharField(blank=True, max_length=2)),
        #         ('alias', models.CharField(db_index=True, max_length=255)),
        #         ('node', models.ForeignKey(to='ninecms.Node')),
        #     ],
        # ),
        # migrations.AlterUniqueTogether(
        #     name='urlalias',
        #     unique_together=set([('language', 'alias')]),
        # ),
        # migrations.RemoveField(
        #     model_name='node',
        #     name='slug',
        # ),
        migrations.AddField(
            model_name='node',
            name='body',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='node',
            name='changed',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 6, 16, 9, 5, 566288, tzinfo=utc),
                                       auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='node',
            name='highlight',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='node',
            name='language',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='node',
            name='original_translation',
            field=models.ForeignKey(to='ninecms.Node', null=True, blank=True, related_name='Translations'),
        ),
        migrations.AddField(
            model_name='node',
            name='promote',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='node',
            name='status',
            field=models.BooleanField(default=1),
        ),
        migrations.AddField(
            model_name='node',
            name='sticky',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='node',
            name='summary',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='node',
            name='title',
            field=models.CharField(default='Default2', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='noderevision',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 3, 6, 16, 9, 37, 798450,
                                                                                    tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='noderevision',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='noderevision',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='noderevision',
            name='revision',
        ),
        migrations.RemoveField(
            model_name='noderevision',
            name='language',
        ),
        migrations.RemoveField(
            model_name='noderevision',
            name='date',
        ),
        migrations.CreateModel(
            name='TaxonomyTerm',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('weight', models.IntegerField(db_index=True, default=0)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('description_node', models.ForeignKey(to='ninecms.Node', null=True, blank=True, related_name='+')),
                ('nodes', models.ManyToManyField(related_name='terms', blank=True, to='ninecms.Node')),
                ('parent', mptt.fields.TreeForeignKey(to='ninecms.TaxonomyTerm', null=True, blank=True,
                                                      related_name='children')),
                ('name', models.CharField(default='', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        # migrations.AlterModelOptions(
        #     name='urlalias',
        #     options={'verbose_name_plural': 'Url aliases'},
        # ),
        migrations.AddField(
            model_name='contentblock',
            name='classes',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='contentblock',
            name='signal',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('group', models.CharField(blank=True, max_length=50)),
                ('file', models.FileField(upload_to=ninecms.models.file_path_file_name,
                                          validators=[ninecms.models.validate_file_ext], max_length=255)),
                ('node', models.ForeignKey(to='ninecms.Node')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('group', models.CharField(blank=True, max_length=50)),
                ('video', models.FileField(upload_to=ninecms.models.video_path_file_name,
                                           validators=[ninecms.models.validate_video_ext], max_length=255)),
                ('node', models.ForeignKey(to='ninecms.Node')),
                ('media', models.CharField(blank=True, max_length=100)),
                ('type', models.CharField(max_length=5, null=True, blank=True, choices=[
                    ('mp4', 'video/mp4'),
                    ('webm', 'video/webm'),
                    ('ogg', 'video/ogg'),
                    ('flv', 'video/flv'),
                    ('swf', 'application/x-shockwave-flash'),
                    ('jpg', 'image/jpeg')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='pagetype',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='node',
            name='link',
            field=models.URLField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='noderevision',
            name='link',
            field=models.URLField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='type',
            field=models.CharField(default='static', max_length=50, choices=[
                ('static', 'Static: link to node'),
                ('menu', 'Menu: render a menu or submenu'),
                ('signal', 'Signal: call site-specific custom render'),
                ('language', 'Language: switch menu'),
                ('user-menu', 'User menu: render a menu with login/register and logout links'),
                ('login', 'Login: render login form'),
                ('search', 'Search: render search form'),
                ('contact', 'Contact: render contact form')]),
        ),
        # migrations.AddField(
        #     model_name='urlalias',
        #     name='redirect',
        #     field=models.CharField(blank=True, max_length=255),
        # ),
        # migrations.AlterField(
        #     model_name='urlalias',
        #     name='node',
        #     field=models.ForeignKey(to='ninecms.Node', null=True, blank=True),
        # ),
        migrations.AlterModelOptions(
            name='node',
            options={'permissions': (
                ('access_toolbar', 'Can access the CMS toolbar'),
                ('use_full_html', 'Can use Full HTML in node body and summary'))},
        ),
        migrations.AddField(
            model_name='node',
            name='alias',
            field=models.CharField(db_index=True, blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='node',
            name='redirect',
            field=models.BooleanField(default=0),
        ),
        # migrations.RunPython(
        #     code=ninecms.migrations.0022_auto_20150416_1454.migrate_alias,
        # ),
        # migrations.RemoveField(
        #     model_name='urlalias',
        #     name='node',
        # ),
        # migrations.DeleteModel(
        #     name='UrlAlias',
        # ),
    ]
