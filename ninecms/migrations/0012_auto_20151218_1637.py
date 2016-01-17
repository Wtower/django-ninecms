# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import mptt.fields
import ninecms.utils.media
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ninecms', '0011_auto_20151202_1400'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contentblock',
            options={'verbose_name': 'content block', 'verbose_name_plural': 'content blocks'},
        ),
        migrations.AlterModelOptions(
            name='file',
            options={'verbose_name': 'file', 'verbose_name_plural': 'files'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'image', 'verbose_name_plural': 'images'},
        ),
        migrations.AlterModelOptions(
            name='menuitem',
            options={'verbose_name': 'menu item', 'verbose_name_plural': 'menu items'},
        ),
        migrations.AlterModelOptions(
            name='node',
            options={'permissions': (('use_full_html', 'Can use Full HTML in node body and summary'), ('view_unpublished', 'Can view unpublished content')), 'verbose_name': 'node', 'verbose_name_plural': 'nodes'},
        ),
        migrations.AlterModelOptions(
            name='noderevision',
            options={'verbose_name': 'node revision', 'verbose_name_plural': 'node revisions'},
        ),
        migrations.AlterModelOptions(
            name='pagelayoutelement',
            options={'verbose_name': 'page layout element', 'verbose_name_plural': 'page layout elements'},
        ),
        migrations.AlterModelOptions(
            name='pagetype',
            options={'ordering': ['id'], 'permissions': (('add_node_pagetype', 'Add node of a specific page type'), ('change_node_pagetype', 'Change node of a specific page type'), ('delete_node_pagetype', 'Delete node of a specific page type')), 'verbose_name': 'page type', 'verbose_name_plural': 'page types'},
        ),
        migrations.AlterModelOptions(
            name='taxonomyterm',
            options={'verbose_name': 'taxonomy term', 'verbose_name_plural': 'taxonomy terms'},
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='menu_item',
            field=mptt.fields.TreeForeignKey(verbose_name='menu item', null=True, to='ninecms.MenuItem', help_text='The related parent menu item related (block type: menu only).', blank=True),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='node',
            field=models.ForeignKey(verbose_name='node', null=True, to='ninecms.Node', help_text='The related node with this block (block type: static only).', blank=True),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='type',
            field=models.CharField(help_text='How to render the block.', max_length=50, default='static', verbose_name='type', choices=[('static', 'Static: link to node'), ('menu', 'Menu: render a menu or submenu'), ('signal', 'Signal: call site-specific custom render'), ('language', 'Language: switch menu'), ('user-menu', 'User menu: render a menu with login/register and logout links'), ('login', 'Login: render login form'), ('search', 'Search: render search form'), ('search-results', 'Search: render search results'), ('contact', 'Contact: render contact form')]),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(validators=[ninecms.utils.media.validate_file_ext], upload_to=ninecms.utils.media.file_path_file_name, max_length=255, verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='file',
            name='group',
            field=models.CharField(max_length=50, blank=True, verbose_name='group'),
        ),
        migrations.AlterField(
            model_name='file',
            name='node',
            field=models.ForeignKey(to='ninecms.Node', verbose_name='node'),
        ),
        migrations.AlterField(
            model_name='file',
            name='title',
            field=models.CharField(max_length=255, blank=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='image',
            name='group',
            field=models.CharField(max_length=50, blank=True, verbose_name='group'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=ninecms.utils.media.image_path_file_name, max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='image',
            name='node',
            field=models.ForeignKey(to='ninecms.Node', verbose_name='node'),
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=255, blank=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='disabled',
            field=models.BooleanField(default=False, verbose_name='disabled'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='language',
            field=models.CharField(max_length=2, blank=True, verbose_name='language', choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')]),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, to='ninecms.MenuItem', related_name='children', verbose_name='parent menu'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='path',
            field=models.CharField(max_length=255, blank=True, verbose_name='path'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='weight',
            field=models.IntegerField(db_index=True, default=0, verbose_name='order weight'),
        ),
        migrations.AlterField(
            model_name='node',
            name='alias',
            field=models.CharField(db_index=True, max_length=255, blank=True, verbose_name='alias'),
        ),
        migrations.AlterField(
            model_name='node',
            name='body',
            field=models.TextField(blank=True, verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='node',
            name='changed',
            field=models.DateTimeField(verbose_name='date changed', auto_now=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='node',
            name='highlight',
            field=models.CharField(max_length=255, blank=True, verbose_name='highlight'),
        ),
        migrations.AlterField(
            model_name='node',
            name='language',
            field=models.CharField(max_length=2, blank=True, verbose_name='language', choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')]),
        ),
        migrations.AlterField(
            model_name='node',
            name='link',
            field=models.URLField(max_length=255, blank=True, verbose_name='link'),
        ),
        migrations.AlterField(
            model_name='node',
            name='original_translation',
            field=models.ForeignKey(blank=True, null=True, to='ninecms.Node', related_name='Translations', verbose_name='original translation'),
        ),
        migrations.AlterField(
            model_name='node',
            name='page_type',
            field=models.ForeignKey(to='ninecms.PageType', verbose_name='page type'),
        ),
        migrations.AlterField(
            model_name='node',
            name='promote',
            field=models.BooleanField(default=0, verbose_name='promoted'),
        ),
        migrations.AlterField(
            model_name='node',
            name='redirect',
            field=models.BooleanField(default=0, verbose_name='redirect'),
        ),
        migrations.AlterField(
            model_name='node',
            name='status',
            field=models.BooleanField(default=1, verbose_name='published'),
        ),
        migrations.AlterField(
            model_name='node',
            name='sticky',
            field=models.BooleanField(default=0, verbose_name='sticky'),
        ),
        migrations.AlterField(
            model_name='node',
            name='summary',
            field=models.TextField(blank=True, verbose_name='summary'),
        ),
        migrations.AlterField(
            model_name='node',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='node',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='node',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='order weight'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='body',
            field=models.TextField(blank=True, verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='created',
            field=models.DateTimeField(verbose_name='date created', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='highlight',
            field=models.CharField(max_length=255, blank=True, verbose_name='highlight'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='link',
            field=models.URLField(max_length=255, blank=True, verbose_name='link'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='log_entry',
            field=models.CharField(max_length=255, blank=True, verbose_name='log entry'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='node',
            field=models.ForeignKey(to='ninecms.Node', verbose_name='node'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='promote',
            field=models.BooleanField(default=0, verbose_name='promoted'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='status',
            field=models.BooleanField(default=1, verbose_name='published'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='sticky',
            field=models.BooleanField(default=0, verbose_name='sticky'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='summary',
            field=models.TextField(blank=True, verbose_name='summary'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='noderevision',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='pagelayoutelement',
            name='block',
            field=models.ForeignKey(to='ninecms.ContentBlock', verbose_name='content block'),
        ),
        migrations.AlterField(
            model_name='pagelayoutelement',
            name='hidden',
            field=models.BooleanField(db_index=True, default=False, verbose_name='hidden'),
        ),
        migrations.AlterField(
            model_name='pagelayoutelement',
            name='page_type',
            field=models.ForeignKey(to='ninecms.PageType', verbose_name='page type'),
        ),
        migrations.AlterField(
            model_name='pagelayoutelement',
            name='region',
            field=models.CharField(help_text='A hard coded region name that is rendered in template index and also used in <a href="https://github.com/Wtower/django-ninecms#theme-suggestions" target="_blank">theme suggestions</a>.', db_index=True, max_length=50, verbose_name='region'),
        ),
        migrations.AlterField(
            model_name='pagelayoutelement',
            name='weight',
            field=models.IntegerField(db_index=True, help_text='Elements with greater number in the same region sink to the bottom of the page.', default=0, verbose_name='order weight'),
        ),
        migrations.AlterField(
            model_name='pagetype',
            name='description',
            field=models.CharField(help_text='Describe the page type.', max_length=255, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='pagetype',
            name='guidelines',
            field=models.CharField(help_text='Provide content submission guidelines for this page type.', max_length=255, blank=True, verbose_name='guidelines'),
        ),
        migrations.AlterField(
            model_name='pagetype',
            name='name',
            field=models.CharField(help_text='Specify a unique page type name. A machine name is recommended if to be used in code.', max_length=100, verbose_name='name', unique=True),
        ),
        migrations.AlterField(
            model_name='taxonomyterm',
            name='description_node',
            field=models.ForeignKey(blank=True, null=True, to='ninecms.Node', related_name='term_described', verbose_name='description node'),
        ),
        migrations.AlterField(
            model_name='taxonomyterm',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='taxonomyterm',
            name='nodes',
            field=models.ManyToManyField(to='ninecms.Node', related_name='terms', blank=True, verbose_name='nodes'),
        ),
        migrations.AlterField(
            model_name='taxonomyterm',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, to='ninecms.TaxonomyTerm', related_name='children', verbose_name='parent term'),
        ),
        migrations.AlterField(
            model_name='taxonomyterm',
            name='weight',
            field=models.IntegerField(db_index=True, default=0, verbose_name='order weight'),
        ),
        migrations.AlterField(
            model_name='video',
            name='group',
            field=models.CharField(max_length=50, blank=True, verbose_name='group'),
        ),
        migrations.AlterField(
            model_name='video',
            name='node',
            field=models.ForeignKey(to='ninecms.Node', verbose_name='node'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=255, blank=True, verbose_name='title'),
        ),
    ]
