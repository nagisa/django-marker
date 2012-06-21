from django.conf import settings

print('Hello')

_marker = getattr(settings, 'MARKER', {})

MARKER = {
    'fatal_import': settings.DEBUG and _marker.get('fatal_import', True),
    'markdown': {
        'html_replace': '<...>',
        'global_extras': [],
        'link_patterns': None
    }
}
