# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ninecms', '0010_auto_20150924_1850'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='node',
            options={'permissions': (('use_full_html', 'Can use Full HTML in node body and summary'), ('view_unpublished', 'Can view unpublished content'))},
        ),
        migrations.AlterModelOptions(
            name='pagetype',
            options={'ordering': ['id'], 'permissions': (('add_node_pagetype', 'Add node of a specific page type'), ('change_node_pagetype', 'Change node of a specific page type'), ('delete_node_pagetype', 'Delete node of a specific page type'))},
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='classes',
            field=models.CharField(max_length=255, blank=True, help_text='Additional CSS classes to append to block.'),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='menu_item',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, to='ninecms.MenuItem', help_text='The related parent menu item related (block type: menu only).'),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='node',
            field=models.ForeignKey(blank=True, null=True, to='ninecms.Node', help_text='The related node with this block (block type: static only).'),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='signal',
            field=models.CharField(max_length=100, blank=True, help_text='The signal name to trigger for a <a href="https://github.com/Wtower/django-ninecms#views" target="_blank">custom view</a> (block type: signal only).'),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='type',
            field=models.CharField(max_length=50, choices=[('static', 'Static: link to node'), ('menu', 'Menu: render a menu or submenu'), ('signal', 'Signal: call site-specific custom render'), ('language', 'Language: switch menu'), ('user-menu', 'User menu: render a menu with login/register and logout links'), ('login', 'Login: render login form'), ('search', 'Search: render search form'), ('search-results', 'Search: render search results'), ('contact', 'Contact: render contact form')], help_text='How to render the block.', default='static'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='language',
            # field=models.CharField(max_length=2, blank=True, choices=[('el', 'Greek')]),
            field=models.CharField(choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')], max_length=2, blank=True),
        ),
        # migrations.AlterField(
        #     model_name='node',
        #     name='language',
        #     field=models.CharField(max_length=2, blank=True, choices=[('el', 'Greek')]),
        # ),
        migrations.AlterField(
            model_name='pagelayoutelement',
            name='region',
            field=models.CharField(max_length=50, help_text='A hard coded region name that is rendered in template index and also used in <a href="https://github.com/Wtower/django-ninecms#theme-suggestions" target="_blank">theme suggestions</a>.', db_index=True),
        ),
        migrations.AlterField(
            model_name='pagelayoutelement',
            name='weight',
            field=models.IntegerField(help_text='Elements with greater number in the same region sink to the bottom of the page.', default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='pagetype',
            name='description',
            field=models.CharField(max_length=255, help_text='Describe the page type.'),
        ),
        migrations.AlterField(
            model_name='pagetype',
            name='guidelines',
            field=models.CharField(max_length=255, blank=True, help_text='Provide content submission guidelines for this page type.'),
        ),
        migrations.AlterField(
            model_name='pagetype',
            name='name',
            field=models.CharField(max_length=100, unique=True, help_text='Specify a unique page type name. A machine name is recommended if to be used in code.'),
        ),
        migrations.AlterField(
            model_name='pagetype',
            name='template',
            field=models.CharField(max_length=255, blank=True, help_text='Custom template name (deprecated).'),
        ),
        migrations.AlterField(
            model_name='pagetype',
            name='url_pattern',
            field=models.CharField(max_length=255, blank=True, help_text='Default pattern for page type, if no alias is specified in node edit. <a href="https://github.com/Wtower/django-ninecms#url-aliases" target="_blank">More info</a>.'),
        ),
    ]
