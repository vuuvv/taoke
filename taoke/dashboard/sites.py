from django.conf.urls import patterns, url, include
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured
from django.template.response import TemplateResponse
from django.contrib.auth.views import login

from taoke.dashboard.controller import Controller
from taoke.dashboard.models import Menu

class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class Dashboard(object):
    def __init__(self, name='dashboard', app_name='dashboard'):
        self._registry = {}
        self.name = name
        self.app_name = app_name

    def register(self, models_or_controllers, **options):
        if isinstance(models_or_controllers, ModelBase) or issubclass(models_or_controllers, Controller):
            models_or_controllers = [models_or_controllers]

        for obj in models_or_controllers:
            if isinstance(obj, ModelBase):
                controller = ModelController
                model = obj
            else:
                controller = obj
                model = controller.model
                if model is None:
                    raise ImproperlyConfigured('You should set model in the '
                        'specified Controller %s.' % controller.__name__)

            if model._meta.abstract:
                raise ImproperlyConfigured('The model %s is abstrace so it '
                      'cannot be registered with dashboard.' % model.__name__)

            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)

            if options:
                pass

            self._registry[model] = controller(self, model)

    def unregister(self, models):
        if isinstance(models, ModelBase):
            models = [models]
        for model in models:
            if model not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name)
            del self._registry[model]

    @property
    def urlpatterns(self):
        urlpatterns = patterns('',
            url(r'^$', self.index, name='dashboard_index'),
            url(r'^logout/$', self.logout, name='dashboard_logout'),
            url(r'^login/$', self.login, name='dashboard_login'),

            url(r'^all_urls/$', self.all_urls, name='show all urls'),
        )

        for model, controller in self._registry.iteritems():
            urlpatterns += patterns('',
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.module_name),
                    include(controller.urls))
            )

        return urlpatterns

    @property
    def urls(self):
        return self.urlpatterns

    def index(self, request):
        top_menus = Menu.objects.root_nodes().filter(visible=True)
        left_menus = top_menus[0].get_children().filter(visible=True).filter(level__lt=3)
        return TemplateResponse(request, 'dashboard/index.html', {
            'top_menus': top_menus,
            'left_menus': left_menus
        })

    def logout(self, request):
        pass

    def login(self, request):
        return login(request, 'dashboard/login.html')

    def all_urls(self, request):
        from django.core import urlresolvers
        from django.http import HttpResponse

        resolver = urlresolvers.get_resolver(None)
        dict = resolver.reverse_dict
        patterns = sorted([
            (key, value[0][0][0])
            for key, value in resolver.reverse_dict.items()
            if isinstance(key, basestring)
        ])

        text = "<table>"
        longest = max([len(pair[0]) for pair in patterns])
        for key, value in patterns:
            text += '<tr><td>%s</td><td>%s</td></tr>\n' % (key.ljust(longest + 1), value)
        text += "</table>"
        return HttpResponse(text)

site = Dashboard()

