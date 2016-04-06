""" Application name of Nine CMS for Admin """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.apps import AppConfig


# noinspection PyUnresolvedReferences
class NineCMSConfig(AppConfig):
    name = 'ninecms'
    verbose_name = "Nine CMS"

    def ready(self):
        import ninecms.signals
        import ninecms.checks
