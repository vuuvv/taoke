from django.conf.urls import patterns, include, url

urlpatterns = patterns('taoke.dashboard.views',
    url(r'^$', 'index', name='dashboard home page'),
)

urlpatterns += patterns('taoke.dashboard.admin_user',
    url(r'^user/$', 'index', name='user list'),
)
