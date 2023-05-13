# django-fragments Docs

Reusable partial templates, originally meant for a Django [boilerplate](https://start-django.fly.dev), refactored out into an independent library.

## Installation

After installation, e.g. `pip install django-fragments`

```py
INSTALLED_APPS = [
    "django_fragments", # add this
]
...
FRAGMENTS = {
    "icons_prefix": "heroicons", # prefix to use for icons
    "icons_path": BASE_DIR / "templates" / "xxx" # type: Path, location where svg icons will be stored
}
```

Invoke via `{% load fragments %}`

## Fragments

??? tip "Notes in using template tags"

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

### Shortcuts

1. [`{% icon %}`](./fragments/icon.md) - idiomatic `<svg>` combiner with neighboring / parent tags
2. [`{% hput %}`](./fragments/hput.md) - encapsulated, [tweakable](https://github.com/jazzband/django-widget-tweaks) `<input>` with option for inline validation.
3. [`{% nava %}`](./fragments/nava.md#nava) - Uses `format_html` to output an `<a>` element fit for desktop/mobile navbar links.
4. [`{% curr %}`](./fragments/nava.md#curr) - Outputs string `aria-current=page` if url is current.

### Open Graph

1. [`{% og_title %}`](./fragments/og.md#og_title) - Formats the meta tags related to the title
2. [`{% og_desc %}`](./fragments/og.md#og_desc) - Formats the meta tags related to the description
3. [`{% og_img %}`](./fragments/og.md#og_img) - Formats the meta tags related to the image

## Architectures

### Message Alerts Template

See [framework](./architectures/msg.md) for applying django messages, htmx, and hyperscript.

### Select Dropdown Base

Example attempted architectures for:

1. [listbox](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/) via a fake [select](./architectures/dropdown.md#listbox). See sample in `down-list.html` - hides (but still uses) a real `<select>` field in the DOM, displaying a styleable alternative. Here the `<ul>` has a role of `listbox` and each child item the role of `option`.

2. [menubar](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/) via [button toggle](./architectures/dropdown.md#menubar). See sample  in `_nav.html` - `<ul>` has a role of `menu` and each child item the role of `menuitem`.

!!! warning "Not yet feature complete."

    Would have preferred hyperscript here but it because too unwieldy so settled with vanilla js. This attempts to replicate the ARIA recommendations but not everything has been adopted (yet).

## Utils

1. [`{% whitespaceless %}`](./utils.md#whitespaceless)
2. [Filtering of Attributes](./utils.md#filter-attributes)
3. [Wrap Icon Processing](./utils.md#wrap-icon)
