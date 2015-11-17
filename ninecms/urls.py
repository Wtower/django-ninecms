""" URL specification for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import RedirectView
from ninecms import views


urlpatterns = [
    # Content

    # Cms landing redirect
    url(r'^cms/$', RedirectView.as_view(pattern_name='admin:index', permanent=True)),
    url(r'^cms/content/$', RedirectView.as_view(pattern_name='admin:ninecms_node_changelist', permanent=True)),

    #  Node id redirect: cms/content/<node-id>
    url(r'^cms/content/(?P<node_id>\d+)/$', views.ContentNodeView.as_view(),
        name="content_node"),

    # Status

    # status page: cms/status
    url(r'^cms/status/$', staff_member_required(views.StatusView.as_view()),
        name='status'),

    # Other forms

    # Contact: contact/form/
    url(r'^contact/form/$', views.ContactView.as_view(),
        name='contact'),

    # Login: user/login/
    url(r'^user/login/$', views.LoginView.as_view(),
        name='login'),

    # Logout: user/logout/
    url(r'^user/logout/$', login_required(views.LogoutView.as_view()),
        name='logout'),

    # Node render

    # Render page: /<slug>
    url(r'^(?P<url_alias>[/\w\-_]+)$', views.AliasView.as_view(),
        name='alias'),

    # Default index: /
    url(r'^$', views.IndexView.as_view(),
        name='index'),
]
