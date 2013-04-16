from functools import partial, wraps
from inspect import ismethod
import json

from django import forms
from django.db import models
from django.http import HttpResponse
from django.forms.models import modelform_factory
from django.conf.urls import patterns, url
from django.template.response import TemplateResponse
from django.core.validators import MaxValueValidator, MaxLengthValidator
from django.utils.translation import ugettext_lazy as _

from taoke.dashboard.models import LogEntry, ADDITION, DELETION, CHANGE
from taoke.dashboard import widgets

FORMFIELD_FOR_DBFIELD_DEFAULTS = {
    models.CharField:       {'widget': widgets.TextBox},
}

def get_validators(form):
    validators = {}
    for name, field in form.fields.iteritems():
        validator = {}
        if field.required:
            validator['min'] = 1
            validator['onerrormin'] = 'Please input %s' % name
        for v in field.validators:
            if isinstance(v, MaxLengthValidator):
                validator['max'] = v.limit_value
                validator['onerror'] = u"%s" % v.message
        if validator:
            validators[name] = u','.join([u'"%s":%s' % (k, u'"%s"' % v if isinstance(v, basestring) else v)for k, v in validator.iteritems()])

    return validators


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
    tools = (
        (_('Add'), True, 'add_url'),
    )

    def __init__(self, site, model):
        self.model = model
        self.site = site

        widgets = FORMFIELD_FOR_DBFIELD_DEFAULTS.copy()
        widgets.update(self.formfield_widgets)
        self.formfield_widgets = widgets

    @property
    def urls(self):
        return self.urlpatterns

    @property
    def add_url(self):
        app, module = self.model._meta.app_label, self.model._meta.module_name
        return '%s_%s_add' % (app, module)

    def _render(self, request, template_name, context):
        opts = self.model._meta
        app_label = opts.app_label

        if "_popup" in request.REQUEST:
            template_name += "_raw"

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

    def get_tools(self):
        tools = []
        for name, popup, url in self.tools:
            tools.append((name, popup, getattr(self, url, url)))
        return tools

    def get_columns(self):
        columns = []
        opts = self.model._meta
        for d in self.list_display:
            columns.append(opts.get_field(d).verbose_name)
        return columns

    def log_addition(self, request, object):
        LogEntry.objects.log_adtion(
            user_id             = request.user.pk,
            content_type_id     = ContentType.objects.get_for_model(object).pk,
            object_id           = object.pk,
            object_repr         = force_unicode(object),
            action_flag         = ADDITION,
        )

    def log_change(self, request, object):
        LogEntry.objects.log_adtion(
            user_id             = request.user.pk,
            content_type_id     = ContentType.objects.get_for_model(object).pk,
            object_id           = object.pk,
            object_repr         = force_unicode(object),
            action_flag         = CHANGE,
            change_message      = message,
        )

    def log_deletion(self, request, object):
        LogEntry.objects.log_adtion(
            user_id             = request.user.pk,
            content_type_id     = ContentType.objects.get_for_model(object).pk,
            object_id           = object.pk,
            object_repr         = force_unicode(object),
            action_flag         = DELETION,
        )

    @route(r'^$')
    def list(self, request):
        if self.list_display:
            objs = self.model.objects.all()
        else:
            objs = self.model.objects.values(*self.list_display)

        return {
            'objs': objs,
            'tools': self.get_tools(),
            'columns': self.get_columns(),
            'list_display': self.list_display,
        }

    @route(r'^add/$')
    def add(self, request):
        form_cls = self.get_form_cls()

        if request.method == 'POST':
            form = form_cls(request.POST, request.FILES)
            if form.is_valid():
                new_object = self.save_form(request, form, change=False)
                self.log_addition(request, new_object)
                return json.dumps({ 'success': True })
            else:
                return json.dumps({ 'success': False, 'errors': form.errors })
        else:
            form = form_cls()

        return {
            'form': form,
            'validators': get_validators(form),
            'form_name': self.model._meta.module_name,
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


