"""
Set of "markup" template filters for Django.  These filters transform plain text
markup syntaxes to HTML; currently there is support for:

    * Markdown, which requires the markdown2 library available at
      https://github.com/trentm/python-markdown
"""
import re

from django import template

from settings import MARKER

register = template.Library()

@register.simple_tag
def markdown(what, **kwargs):
    """
    Parses given value with markdown, optionally using extras documented at
    https://github.com/trentm/python-markdown2/wiki/Extras.

    Syntax::

        {% markdown text %}
        {% markdown text extras="code-friendly,fenced-code-blocks" %}
        {% markdown text safe_mode="escape" %} or safe_mode="replace"


    Extras can also be enabled globally by adding variable in settings.py.
    """
    try:
        import markdown2
    except ImportError:
        if MARKER['fatal_import']:
            raise template.TemplateSyntaxError('Could not import markdown2.')
        return what

    extras = MARKER['markdown']['global_extras'] + \
                                            kwargs.get('extras', '').split(',')

    md = markdown2.Markdown(safe_mode=kwargs.get('safe_mode', False),
                            extras=set(extras),
                            link_patterns=MARKER['markdown']['link_patterns'])
    # Safe mode. Possible values are escape and replace. You can set replacement
    # in global settings.
    md.html_removed_text = MARKER['markdown']['html_replace']

    return md.convert(what)
