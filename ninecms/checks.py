""" NineCMS system checks """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'

from django.core.checks import register, Tags, Info
from django.conf import settings


# noinspection PyUnusedLocal
@register(Tags.compatibility)
def check_settings(app_configs, **kwargs):
    """ Check that settings are implemented properly for 9cms
    :param app_configs: a list of apps to be checks or None for all
    :param kwargs: keyword arguments
    :return: a list of errors
    """
    checks = []
    if not settings.MEDIA_ROOT:
        msg = ("No media root is specified in settings. A media folder is necessary for the user to upload images. "
               "You can specify one in the settings file as eg: `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`.")
        checks.append(Info(msg, id='ninecms.I001'))
    if not settings.MEDIA_URL:
        msg = ("No media url is specified in settings. A media url is necessary for 9cms to display uploaded images. "
               "You can specify one in the settings file as eg: `MEDIA_URL = '/media/'`.")
        checks.append(Info(msg, id='ninecms.I002'))
    if not settings.ADMINS:
        msg = ("No administrator emails are specified in settings. These are necessary for 9cms to send information "
               "on updates if a cron is setup. You can specify them in the settings file as eg: "
               "`ADMINS = (('Webmaster', 'web@9-dev.com'),)`.")
        checks.append(Info(msg, id='ninecms.I003'))
    if not settings.MANAGERS:
        msg = ("No manager emails are specified in settings. These are necessary for 9cms to messages through the "
               "contact form. You can specify them in the settings file as eg: "
               "`MANAGERS = (('Webmaster', 'web@9-dev.com'),)`.")
        checks.append(Info(msg, id='ninecms.I004'))
    if settings.SESSION_COOKIE_NAME == 'sessionid':
        msg = ("It is advised that you specify a session cookie name other than the default, especially in shared "
               "hosting environments. You can specify this in the settings file as eg: "
               "`SESSION_COOKIE_NAME = 'myapp_sessionid'`.")
        checks.append(Info(msg, id='ninecms.I005'))
    if settings.CACHES['default']['BACKEND'] == 'django.core.cache.backends.memcached.MemcachedCache':
        if not settings.CACHES['default']['KEY_PREFIX']:
            msg = ("It is advised that you specify a cache key prefix for the default memcached, especially in shared "
                   "hosting environments. You can specify this in the settings file with "
                   "``settings.CACHES['default']['KEY_PREFIX']`.")
            checks.append(Info(msg, id='ninecms.I006'))
    return checks
