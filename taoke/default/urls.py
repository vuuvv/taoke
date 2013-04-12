from django.conf.urls import patterns, include, url

from taoke.dashboard.sites import site
from taoke.dashboard import controllers

urlpatterns = patterns('taoke.default.views',
    url(r'^$', 'index', name='home page'),
    url(r'^dashboard/', include(site.urls)),
)
