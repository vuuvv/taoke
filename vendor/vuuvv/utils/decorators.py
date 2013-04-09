from django.http import HttpResponse
from django.template.response import TemplateResponse

class TemplateView(object):
    def __init__(self, func):
        pass

    def __call__(self):
        pass


def template(func):
    dir = func.__module__.split(".")[-2]
    tmpl = '%s/%s.html' % (dir, func.__name__)
    def _func(request, *a, **kw):
        result = func(request, *a, **kw)
        if isinstance(result, basestring):
            return HttpResponse(result)
        else:
            return TemplateResponse(request, tmpl, result)

    return _func
