# django-marker

## Why?

First of all, `contrib.markup`
[is getting deprecated](https://code.djangoproject.com/ticket/18054), it has
issues with security and rendering.

It is a pretty good time to start this project to avoid a panic of community,
when actual deprecation warning appears in release notes.

## What do I get?

Our primary goal is to provide template tags for same three markups that are
provided by `contrib.markup`.

## How to use?

```django
{% load marker %}

{# Use one of available tags... #}
{% markdown your_text %}
```

Additional documentation for:

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

Misaka is fastest out of all tested Python libraries. Also it uses
security-focused [sundown](http://blog.vmarti.net/sundown/) which makes it a
good choice for most of your markdown needs.

```
   Misaka: 0.07s
cMarkdown: 0.11s
 Discount: 0.21s
    Mark3: 1.32s
 Markdown: 6.87s
Markdown2: 12.42s
```
