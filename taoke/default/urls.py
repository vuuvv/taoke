from django.conf.urls import patterns, include, url

urlpatterns = patterns('taoke.default.views',
    url(r'^$', 'index', name='home page'),
)
