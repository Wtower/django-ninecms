""" Management command for checking updates """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.core.management import BaseCommand
from django.core.cache import caches
from django.core.mail import mail_admins
from django.template import loader
from django.utils.translation import ugettext as _
from ninecms.utils.status import Capturing
# noinspection PyPackageRequirements
import pip


class Command(BaseCommand):
    help = "Check for updates, store the results to cache and send email to admins."

    def handle(self, *args, **options):
        """ Core function
        :param args: None
        :param options: None
        :return: None
        """
        with Capturing() as updates:
            pip.main(['list', '--outdated', '--retries', '1'])
        cache = caches['default']
        if not updates:  # pragma: nocover
            cache.delete('updates')
        else:  # pragma: nocover
            cache.set('updates', updates, 7 * 24 * 60 * 60)  # 1wk
            t = loader.get_template('ninecms/mail_updates.txt')
            mail_admins(_("New updates available"), t.render({'updates': updates}))
