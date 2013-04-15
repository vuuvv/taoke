from functools import partial, wraps
from inspect import ismethod

from django import forms
from django.db import models
from django.http import HttpResponse
from django.forms.models import modelform_factory
from django.conf.urls import patterns, url
from django.template.response import TemplateResponse

from taoke.dashboard import widgets

FORMFIELD_FOR_DBFIELD_DEFAULTS = {
    models.CharField:       {'widget': widgets.TextBox},
}

def urlpatterns_property(cls):
    def _urlpatterns(self):
        views = []
        for attr in dir(cls):
            v = getattr(cls, attr)
            if ismethod(v) and hasattr(v, 'pattern'):
                views.append((attr, v))

        app, module = self.model._meta.app_label, self.model._meta.module_name

        args = []
        for name, func in views:
            _func = wraps(func)(partial(func, self))
            args.append(url(func.pattern, _func, name='%s_%s_%s' %
                            (app, module, name)))

        return patterns('', *args)

    return property(_urlpatterns)

def route(pattern):
    def _route(func):
        @wraps(func)
        def _func(self, request, *args, **kwargs):
            context = func(self, request, *args, **kwargs)
            if isinstance(context, basestring):
                return HttpResponse(context)
            else:
                template = context.get('template', func.__name__)
                return self._render(request, template, context)
        _func.pattern = pattern
        return _func
    return _route

class ViewsFinderMetaClass(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(ViewsFinderMetaClass, cls).__new__(cls, name, bases, attrs)
        new_class.urlpatterns = urlpatterns_property(new_class)
        return new_class

class Controller(object):
    __metaclass__ = ViewsFinderMetaClass

    model = None
    fields = None
    list_display = ('__str__', )
    filter = ()

    form = forms.ModelForm
    formfield_widgets = {}

    buttons = ()

    def __init__(self, site, model):
        self.model = model
        self.site = site

        widgets = FORMFIELD_FOR_DBFIELD_DEFAULTS.copy()
        widgets.update(self.formfield_widgets)
        self.formfield_widgets = widgets

    @property
    def urls(self):
        return self.urlpatterns

    def _render(self, request, template_name, context):
        opts = self.model._meta
        app_label = opts.app_label

        return TemplateResponse(request, [
            'dashboard/%s/%s/%s.html' % (template_name, opts.object_name.lower(), template_name),
            'dashboard/%s/%s.html' %  (app_label, template_name),
            'dashboard/%s.html' % template_name
        ], context)

    def formfield_for_dbfield(self, db_field, **kwargs):
        for cls in db_field.__class__.mro():
            if cls in self.formfield_widgets:
                kwargs = dict(self.formfield_widgets[cls], **kwargs)
                return db_field.formfield(**kwargs)
        return db_field.formfield(**kwargs)

    def get_form_cls(self):
        defaults = {
            'form': self.form,
            'fields': self.fields,
            'formfield_callback': self.formfield_for_dbfield,
        }
        return modelform_factory(self.model, **defaults)

    @route(r'^$')
    def list(self, request):
        pass

    @route(r'^add/$')
    def add(self, request):
        form_cls = self.get_form_cls()
        form = form_cls()
        #return form.as_p()
        return {
            'form': form,
            'template': 'edit',
        }

    @route(r'^(.+)/$')
    def edit(self, request, id):
        pass

    @route(r'^(.+)/delete/$')
    def delete(self, request):
        pass

    @route(r'^(.+)/history/$')
    def history(self, request):
        pass


