from django.conf.urls import patterns, url
from django.template.response import TemplateResponse

class Controller(object):

    model = None
    fields = None
    list_display = ('__str__', )
    filter = ()

    buttons = ()

    def __init__(self, site, model):
        self.model = model
        self.site = site

    @property
    def urlpatterns(self):
        info = self.model._meta.app_label, self.model._meta.module_name

        return patterns('',
            url(r'^$', self.list, name='%s_%s_list' % info),
            url(r'^add/$', self.add, name='%s_%s_add' % info),
            url(r'^(.+)/history/$', self.history, name='%s_%s_history' % info),
            url(r'^(.+)/delete/$',self.delete, name='%s_%s_delete' % info),
            url(r'^(.+)/$', self.edit, name='%s_%s_edit' % info),
        )

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
        ])

    def list(self, request):
        context = {}
        return self._render(request, "list", context)

    def add(self, request):
        context = {}
        return self._render(request, "edit", context)

    def edit(self, request):
        context = {}
        return self._render(request, "edit", context)

    def delete(self, request):
        pass

    def history(self, request):
        context = {}
        return self._render(request, "history", context)


