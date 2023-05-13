# django-fragments Docs

!!! danger "In active development"

    Expect breaking changes.

??? tip "Invoke via `{% load fragments %}` but note conventions"

    Some notes from [:simple-django:](https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#django.template.Library.simple_tag):

    1. Checking for the required number of arguments, etc., has already been done by the time our function is called, so we don’t need to do that.
    2. The quotes around the argument (if any) have already been stripped away, so we receive a plain string.
    3. If the argument was a template variable, our function is passed the current value of the variable, not the variable itself.

    ```jinja title="Simple tag conventions"
    {% icon
      name='x_mark_mini'
      parent_title="{{variable}}"
    %}
    {# won't work, multiline tags are not supported in Django #}

    {% icon name='x_mark_mini' parent_title="{{variable}}" %}
    {# won't work, the variable needs to be passed directly #}

    {% icon name='x_mark_mini' parent_title=variable %}
    {# works #}

    {% with variable='This is a title' %}
      {% icon name='x_mark_mini' parent_title=variable %}
    {% endwith %}
    {# works #}
    ```

## Shortcuts

fragment | note
--:|:--
[`{% themer %}`](./fragments/themer.md) | overrideable theme switcher, affecting `<html class=?>`
[`{% icon %}`](./fragments/icon.md) | idiomatic `<svg>` combiner with neighboring / parent tags
[`{% hput %}`](./fragments/hput.md) | optional inline validated `<input>`, is [widget-tweakable](https://github.com/jazzband/django-widget-tweaks)
[`{% nava %}`](./fragments/nava.md#nava) | Uses [`format_html`](https://docs.djangoproject.com/en/dev/ref/utils/#django.utils.html.format_html) to output an `<a>` element fit for desktop/mobile navbar links
[`{% curr %}`](./fragments/nava.md#curr) | Outputs string `aria-current=page` if url is current

## Open Graph

fragment | note
--:|:--
[`{% og_title %}`](./fragments/og.md#og_title) | Adds to `<title>` and related open graph tags
[`{% og_desc %}`](./fragments/og.md#og_desc) | Adds to `<meta name=description>` and related open graph tags
[`{% og_img %}`](./fragments/og.md#og_img) | Adds image-related open graph tags

## Helpers

fragment | note
--:|:--
[`{% whitespaceless %}`](./utils.md#whitespaceless) | Remove _"space between tags and text"_, outside [{% spaceless %}](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#spaceless) scope.
[`{% htmx_csrf %}`](./utils.md#htmx_csrf) | Adds idiomatic `hx-header=csrf-token-variable`

These are partial templates, originally meant for a Django [boilerplate](https://start-django.fly.dev), refactored out as independent library.

## Extra Utils

1. [is_htmx](./utils.md#is_htmx)
2. [Filtering of Attributes](./utils.md#filter-attributes)
3. [Wrap Icon Processing](./utils.md#wrap-icon)
