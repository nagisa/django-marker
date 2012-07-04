"""
Set of "markup" template filters for Django.  These filters transform plain text
markup syntaxes to HTML; currently there is support for:

    * Markdown, which requires the misaka library available at PyPI.
      Project page is at http://misaka.61924.nl/.

    * reST, which requires the docutils library available at PyPI.
      Project page is at http://docutils.sourceforge.net/
"""
from django import template

from settings import MARKER

register = template.Library()


@register.simple_tag
def markdown(value, **kwargs):
    """
    Parses given value with markdown, optionally using some extensions.

    Syntax::

        {% markdown value %}
        {% markdown value exts="fenced-code,autolink" %}
        {% markdown value html="escape" %}

    You can find value each option does at http://misaka.61924.nl/api/#toc_0.

    Extensions and HTML flags can also be enabled globally by adding variable
    in settings.py.
    """
    def get_flag(strs, prefix):
        flag = 0
        for string in strs:
            if string.strip() == '':
                continue
            var = "{0}_{1}".format(prefix, string.replace('-', '_').upper())
            if hasattr(misaka, var):
                flag |= getattr(misaka, var)
            else:
                raise ValueError, 'Could not find {0} in misaka'.format(string)
        return flag

    try:
       import misaka
    except ImportError:
        if MARKER['fatal_import']:
            raise ImportError('Error in \'markdown\' filter:' \
                              ' Could not import \'misaka\' library.')
        return value
    else:
        exts = MARKER['markdown']['global_exts']
        exts = set(exts + kwargs.get('exts', '').split(','))

        html = MARKER['markdown']['global_html']
        html = set(html + kwargs.get('html', '').split(','))

        return misaka.html(value, extensions=get_flag(exts, 'EXT'),
                           render_flags=get_flag(html, 'HTML'))


@register.simple_tag
def restructuredtext(value, **kwargs):
    """
    Parses given value with restructuredtext.

    Syntax::

        {% restructuredtext value %}
        {% restructuredtext value settings="initial_header_level:2" %}

    Settings argument takes a string of comma separated `key:value` pairs.

    Note::

        If you want to disable option, leave value empty, for example: 
        settings="compact_lists:,initial_header_value:2".

    You can also set settings globally by adding MARKER['restructuredtext']
    in your settings.py

    Consult with
    http://docutils.sourceforge.net/docs/user/config.html#html4css1-writer for
    available settings and values.
    """
    try:
        from docutils.core import publish_parts
    except ImportError:
        if MARKER['fatal_import']:
            raise ImportError('Error in \'restructuredtext\' filter:' \
                              ' Could not import \'docutils\' library.')
        return value
    else:
        settings = MARKER['restructuredtext'].copy()
        for setting in kwargs.get('settings', '').split(','):
            if setting.strip() == '':
                continue
            else:
                key, setting = setting.split(':')
                setting = setting.strip()
                settings[key.strip()] = setting

    parts = publish_parts(source=value, writer_name='html4css1',
                          settings_overrides=settings)
    return parts['fragment']

