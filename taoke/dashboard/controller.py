from functools import partial, wraps
from inspect import ismethod
import json

from django import forms
from django.db import models, transaction
from django.http import HttpResponse, Http404
from django.forms.models import modelform_factory
from django.conf.urls import patterns, url
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, resolve
from django.core.validators import MaxValueValidator, MaxLengthValidator
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.util import unquote
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django.utils.text import get_text_list

from mptt.models import MPTTModel

from taoke.dashboard.models import Menu, LogEntry, ADDITION, DELETION, CHANGE
from taoke.dashboard import widgets

FORMFIELD_FOR_DBFIELD_DEFAULTS = {
    models.CharField:       {'widget': widgets.TextBox},
}

csrf_protect_m = method_decorator(csrf_protect)

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
    list_display_action = (
        (_('Edit'), True, 'edit_url'),
        (_('Delete'), True, 'delete_url'),
    )
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
        return reverse('%s_%s_add' % (app, module))

    def edit_url(self, obj):
        app, module = self.model._meta.app_label, self.model._meta.module_name
        return reverse('%s_%s_edit' % (app, module), args=(obj.id, ))

    def delete_url(self, obj):
        app, module = self.model._meta.app_label, self.model._meta.module_name
        return reverse('%s_%s_delete' % (app, module), args=(obj.id, ))


    def _render(self, request, template_name, context):
        opts = self.model._meta
        app_label = opts.app_label

        template_name = self.get_template_name(template_name)

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

    def save_form(self, request, form):
        return form.save()

    def get_template_name(self, template_name):
        if issubclass(self.model, MPTTModel) and template_name == 'list':
            return 'tree%s' % template_name
        return template_name

    def get_form_cls(self):
        defaults = {
            'form': self.form,
            'fields': self.fields,
            'formfield_callback': self.formfield_for_dbfield,
        }
        return modelform_factory(self.model, **defaults)

    def get_object(self, object_id):
        model = self.model
        try:
            object_id = model._meta.pk.to_python(object_id)
            return model.objects.get(pk=object_id)
        except (model.DoesNotExist, ValidationError):
            return None

    def get_tools(self):
        tools = []
        for name, popup, url in self.tools:
            tools.append((name, popup, getattr(self, url, url)))
        return tools

    def get_list_display_action(self, objs):
        ret = []
        for obj in objs:
            actions = []
            for a in self.list_display_action:
                name, popup, callback = a
                callback = getattr(self, callback, callback)
                if callable(callback):
                    callback = callback(obj)
                actions.append((name, popup, callback))

            ret.append({
                'item': obj,
                'actions': actions
            })
        return ret

    def get_columns(self):
        columns = []
        opts = self.model._meta
        for d in self.list_display:
            columns.append(opts.get_field(d).verbose_name)
        return columns

    def log_addition(self, request, object):
        LogEntry.objects.log_action(
            user_id             = request.user.pk,
            content_type_id     = ContentType.objects.get_for_model(object).pk,
            object_id           = object.pk,
            object_repr         = force_unicode(object),
            action_flag         = ADDITION,
        )

    def log_change(self, request, object, message):
        LogEntry.objects.log_action(
            user_id             = request.user.pk,
            content_type_id     = ContentType.objects.get_for_model(object).pk,
            object_id           = object.pk,
            object_repr         = force_unicode(object),
            action_flag         = CHANGE,
            change_message      = message,
        )

    def log_deletion(self, request, object):
        LogEntry.objects.log_action(
            user_id             = request.user.pk,
            content_type_id     = ContentType.objects.get_for_model(object).pk,
            object_id           = object.pk,
            object_repr         = force_unicode(object),
            action_flag         = DELETION,
        )

    def construct_change_message(self, request, form):
        change_message = []
        if form.changed_data:
            change_message.append(_('Changed %s.') % get_text_list(form.changed_data, _('and')))
        return change_message or _('No fields changed.')

    @route(r'^$')
    def list(self, request):
        if self.list_display:
            objs = self.model.objects.all()
        else:
            objs = self.model.objects.values(*self.list_display)

        objs = self.get_list_display_action(objs)

        context =  {
            'objs': objs,
            'tools': self.get_tools(),
            'columns': self.get_columns(),
            'list_display': self.list_display,
            'table_id': '%s_table_list' % self.model._meta.module_name,
        }

        view = resolve(request.path_info).url_name
        menu = Menu.objects.get(view=view)

        return json.dumps({
            'success': True,
            'title': menu.name,
            'id': menu.id,
            'content': self._render(request, 'list', context).rendered_content,
        })

    @route(r'^add/$')
    @csrf_protect_m
    @transaction.commit_on_success
    def add(self, request):
        form_cls = self.get_form_cls()

        if request.method == 'POST':
            form = form_cls(request.POST, request.FILES)
            if form.is_valid():
                new_object = self.save_form(request, form)
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
    @csrf_protect_m
    @transaction.commit_on_success
    def edit(self, request, id):
        model = self.model
        opts = model._meta

        obj = self.get_object(unquote(id))

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        form_cls = self.get_form_cls()

        if request.method == 'POST':
            form = form_cls(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                new_object = self.save_form(request, form)
                change_message = self.construct_change_message(request, form)
                self.log_change(request, new_object, change_message)
                return json.dumps({ 'success': True })
            else:
                return json.dumps({ 'success': False, 'errors': form.errors })
        else:
            form = form_cls(instance=obj)

        return {
            'form': form,
            'validators': get_validators(form),
            'form_name': opts.module_name,
            'template': 'edit',
        }

    @route(r'^(.+)/delete/$')
    def delete(self, request):
        pass

    @route(r'^(.+)/history/$')
    def history(self, request):
        pass

