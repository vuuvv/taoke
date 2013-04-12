from vuuvv.utils.decorators import template

@template
def index(request):
    return None

@template
def urls(request):
    patterns = _get_named_patterns();
    text = ""
    longest = max([len(pair[0]) for pair in patterns])
    for key, value in patterns:
        text += '%s %s\n' % (key.ljust(longest + 1), value)
    return text

def _get_named_patterns():
    from django.core import urlresolvers

    resolver = urlresolvers.get_resolver(None)
    patterns = sorted([
        (key, value[0][0][0])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, basestring)
    ])
    return patterns
