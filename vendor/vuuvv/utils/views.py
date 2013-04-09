import sys

from django.http import Http404
from django.conf import settings

DEFAULT_ROUTE_APP = 'home'
DEFAULT_ROUTE_VIEW = 'index'

def get_view(app_name, view):
    try:
        module_name = '%s.%s.%s' % (settings.APP_PREFIX, app_name, 'views')
    except AttributeError:
        raise Http404('You must define APP_PREFIX in setting module!')

    try:
        module = __import__(module_name)
        return getattr(module, view)
    except ImportError:
        raise Http404('No module named %s' % module_name)
    except AttributeError, e:
        raise Http404('View "%s" not defined in %s' % (view, module_name))

def convention_view(request, app, view):
    """
    Add the following pattern to project's urls.py:
        url(r'(?P<app>\w+)?/?(?P<view>\w+)?', convention_view),
    You can set your DEFAULT_ROUTE_VIEW and DEFAULT_ROUTE_APP in django 
    setting file.
    """
    convention_app = getattr(settings, 'DEFAULT_ROUTE_APP', DEFAULT_ROUTE_APP)
    convention_view = getattr(settings, 'DEFAULT_ROUTE_VIEW', DEFAULT_ROUTE_VIEW)
    app = app or convention_app
    view = view or convention_view
    app, view = app.lower(), view.lower()

    return get_view(app, view)(request)

