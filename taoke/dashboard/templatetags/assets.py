from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(name='js')
def js(path):
    return '<script src="%sjs/%s.js" type="text/javascript"></script>' % (
        settings.STATIC_URL, path)

@register.simple_tag(name='js_vendor')
def js_vendor(path):
    return '<script src="%sjs/vendor/%s.js" type="text/javascript"></script>' % (
        settings.STATIC_URL, path)

@register.simple_tag(name='css')
def css(path):
    return '<link media="all" rel="stylesheet" href="%scss/%s.css" type="text/css" />' % (
        settings.STATIC_URL, path)

@register.simple_tag(name='css_vendor')
def css_vendor(path):
    return '<link media="all" rel="stylesheet" href="%scss/vendor/%s.css" type="text/css" />' % (
        settings.STATIC_URL, path)

#TODO: more smart tags, filters, tell debug mode

