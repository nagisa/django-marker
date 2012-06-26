"""
Set of "markup" template filters for Django.  These filters transform plain text
markup syntaxes to HTML; currently there is support for:

    * Markdown, which requires the misaka library available at PyPI.
      Project page is at http://misaka.61924.nl/.
"""
from django import template

from settings import MARKER

register = template.Library()

@register.simple_tag
def markdown(what, **kwargs):
    """
    Parses given value with markdown, optionally using some extensions.

    Syntax::

        {% markdown text %}
        {% markdown text exts="fenced-code,autolink" %}
        {% markdown text html="escape" %}

    You can find what each option does at http://misaka.61924.nl/api/#toc_0.

    Extensions and HTML flags can also be enabled globally by adding variable
    in settings.py.
    """
    try:
       import misaka
    except ImportError:
        if MARKER['fatal_import']:
            raise ImportError('Could not import misaka.')
        return what

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

    exts = MARKER['markdown']['global_exts'] + kwargs.get('exts', '').split(',')
    html = MARKER['markdown']['global_html'] + kwargs.get('html', '').split(',')

    return misaka.html(what, extensions=get_flag(set(exts), 'EXT'),
                       render_flags=get_flag(set(html), 'HTML'))
