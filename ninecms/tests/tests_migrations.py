"""
Test migrations for Nine CMS

https://www.caktusgroup.com/blog/2016/02/02/writing-unit-tests-django-migrations/

This doesn't work at all, to be removed in next commit
"""
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.apps import apps
from django.test import TransactionTestCase
from django.db.migrations.executor import MigrationExecutor
from django.db import connection


class TestMigrations(TransactionTestCase):
    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    migrate_from = None
    migrate_to = None

    def setUp(self):
        assert self.migrate_from and self.migrate_to, \
            "TestCase '{}' must define migrate_from and migrate_to properties".format(type(self).__name__)
        self.migrate_from = [(self.app, self.migrate_from)]
        self.migrate_to = [(self.app, self.migrate_to)]
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to the original migration
        executor.migrate(self.migrate_from)

        self.setUpBeforeMigration(old_apps)

        # Run the migration to test
        executor.migrate(self.migrate_to)

        self.apps = executor.loader.project_state(self.migrate_to).apps

    def setUpBeforeMigration(self, apps):
        pass


class Test0009(TestMigrations):

    migrate_from = '0008_auto_20150819_1516'
    migrate_to = '0009_auto_20150924_1456'

    def setUpBeforeMigration(self, apps):
        pass
        # BlogPost = apps.get_model('blog', 'Post')
        # self.post_id = BlogPost.objects.create(
        #     title = "A test post with tags",
        #     body = "",
        #     tags = "tag1 tag2",
        # ).id

    def test_0009(self):
        pass
        # BlogPost = self.apps.get_model('blog', 'Post')
        # post = BlogPost.objects.get(id=self.post_id)
        #
        # self.assertEqual(post.tags.count(), 2)
        # self.assertEqual(post.tags.all()[0].name, "tag1")
        # self.assertEqual(post.tags.all()[1].name, "tag2")
