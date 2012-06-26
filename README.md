## Why?

First of all, `contrib.markup`
[is getting deprecated](https://code.djangoproject.com/ticket/18054), it has
issues with security and rendering.

It is a pretty good time to start this project to avoid a panic of community,
when actual deprecation warning appears in release notes.

## What do I get?

Our primary goal is to provide template tags for same three markups that are
provided by `contrib.markup`.

Tag syntax, however, is not backwards compatible. It was pretty hard to decide
to drop compatibility for flexibility.

## How to install/use/migrate?

TODO: package module properly and upload it to PyPI.

    pip install ??????

---

Add `marker` to `INSTALLED_APPS` in `settings.py`

```django
{% load marker %}

{# Use one of available tags... #}
{% markdown your_text %}
```

Additional documentation and instructions for:

* [markdown tag](#markdown)

## Markdown

**NOTE**: API (especially extension names) is bound to change soon. See
[misaka's issue #16](https://github.com/FSX/misaka/issues/16).

```django
{# You can enable extensions and render flags via tag #}
{% markdown exts="tables,fenced-code,superscript" html="smartypants,safelink" %}

{# You can find all available options at http://misaka.61924.nl/api/#toc_1 #}
{# To use in tag, strip down EXT_/HTML_ part, and replace _ with -. #}
```

Also you can enable extensions and render flags on global basis, by setting
variable in your `settings.py`.

```python
MARKER = {
    'markdown': {
        'global_exts': ['strikethrough', 'superscript'],
        'global_html': ['hard-wrap']
    }
}
```

#### Why misaka?

Misaka is fastest out of all tested Python libraries. Also it is using
security-focused [sundown](http://blog.vmarti.net/sundown/) as backend which
makes it a good choice for most of your markdown needs.

```
   Misaka: 0.07s
cMarkdown: 0.11s
 Discount: 0.21s
    Mark3: 1.32s
 Markdown: 6.87s
Markdown2: 12.42s
```

#### Migrating from contrib.markup markdown tag.

1.  `skip-html` and `safelink` render flags should provide you with same ammount
    of security, `safe` flag is supposed to provide in `contrib.markup` tag.

2.  Some extensions present in python-markdown doesn't exist in sundown. Namely:

    * abbr
    * attr_list
    * codehilite – *you can achieve same results by using custom renderer.*
    * def_list
    * footnotes
    * meta
    * rss – *wait, what?*
    * wikilinks

    You'll have to sacrifice functionality they provide for security and speed
    gains.


