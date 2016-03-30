"""
ninecms tests URL Configuration
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^robots\.txt/$', TemplateView.as_view(template_name='ninecms/robots.txt', content_type='text/plain')),
]

# static files (images, css, javascript, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # pragma: no cover

# Last: all remaining pass to CMS
if settings.I18N_URLS:  # pragma: nocover
    urlpatterns += i18n_patterns(
        url(r'^', include('ninecms.urls', namespace='ninecms')),
    )
else:  # pragma: nocover
    urlpatterns += [
        url(r'^', include('ninecms.urls', namespace='ninecms')),
    ]
