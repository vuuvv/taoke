from django.conf.urls import patterns, include, url

urlpatterns = patterns('taoke.default.views',
    url(r'^$', 'index', name='home page'),
    url(r'^dashboard/', include('taoke.dashboard.urls')),
)
