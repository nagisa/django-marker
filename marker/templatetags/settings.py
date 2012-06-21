from django.conf import settings

_marker = getattr(settings, 'MARKER', {})
_markdown = _marker.get('markdown', {})

MARKER = {
    'fatal_import': settings.DEBUG and _marker.get('fatal_import', True),
    'markdown': {
        'html_replace': _markdown.get('html_replace', '<...>'),
        'global_extras': _markdown.get('global_extras', []),
        'link_patterns': _markdown.get('link_patterns', None),
    },

}
