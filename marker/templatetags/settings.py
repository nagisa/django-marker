from django.conf import settings

_marker = getattr(settings, 'MARKER', {})
_markdown = _marker.get('markdown', {})

MARKER = {
    'fatal_import': settings.DEBUG and _marker.get('fatal_import', True),
    'markdown': {
        'global_html': _markdown.get('global_html', []),
        'global_exts': _markdown.get('global_exts', []),
    },
}
