""" Management command for clearing cache """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.core.management import BaseCommand
from ninecms.utils.status import cache_clear


class Command(BaseCommand):
    help = "Clears the cache."

    def handle(self, *args, **options):
        """ Core function
        :param args: None
        :param options: None
        :return: None
        """
        cache_clear()
        self.stdout.write("Cache cleared.")
