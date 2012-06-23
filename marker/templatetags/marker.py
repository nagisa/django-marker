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
        {% markdown text ext="fenced-code,autolink" %}
        {% markdown text html="escape" %}

    Possible arguments and values::

        ext="no-intra-emphasis,tables,fenced-code,autolink,strikethrough,
             lax-html-blocks,space-headers,superscript"
        html="skip-html,skip-style,skip-images,skip-links,safelink,toc,
              hard-wrap,use-xhtml,escape,smartypants,toc-tree"

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

    exts = MARKER['markdown']['global_ext'] + kwargs.get('ext', '').split(',')
    html = MARKER['markdown']['global_html'] + kwargs.get('html', '').split(',')

    return misaka.html(what, extensions=exts, render_flags=html)


