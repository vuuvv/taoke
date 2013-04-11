from functools import update_wrapper

from django.conf.urls import patterns, url

class DashboardView(object):
    def __init__(self, category, model_cls):
        self.category = category
        self.model_cls = model_cls

    def index(self):
        pass

    def add(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass

    def search(self):
        pass

    def get_urls(self):
        def wrap(view):
            def _func(*args, **kwargs):
                pass
            return update_wrapper(wrapper, view)

        info = self.category, self.model._meta.module_name

        return patterns('',
            url(r'^$',
                wrap(self.index),
                name='%s_%s_list' % info),
            url(r'^add/$',
                wrap(self.add),
                name='%s_%s_add' % info),
            url(r'^(.+)/history/$',
                wrap(self.history),
                name='%s_%s_history' % info),
            url(r'^^(.+)/delete/$',
                wrap(self.delete),
                name='%s_%s_delete' % info),
            url(r'^(.+)/$',
                wrap(self.edit),
                name='%s_%s_edit' % info),
        )


@template
def index(request):
    return "Hello world"
