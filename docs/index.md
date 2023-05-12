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

### Shortcuts

1. [`{% icon %}`](./icon.md) - idiomatic `<svg>` combiner with neighboring / parent tags
2. [`{% hput %}`](./hput.md) - encapsulated, [tweakable](https://github.com/jazzband/django-widget-tweaks) `<input>` with option for inline validation.
3. [`{% nava %}`](./nava.md#nava) - Uses `format_html` to output an `<a>` element fit for desktop/mobile navbar links.
4. [`{% curr %}`](./nava.md#curr) - Outputs string `aria-current=page` if url is current.

### Open Graph

1. [`{% og_title %}`](./og.md#og_title) - Formats the meta tags related to the title
2. [`{% og_desc %}`](./og.md#og_desc) - Formats the meta tags related to the description
3. [`{% og_img %}`](./og.md#og_img) - Formats the meta tags related to the image

## Select Dropdown Base

Example attempted architectures for [listbox](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/) and [menubar](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/):

```jinja title="{{idx}} needs button, ul, child li options"
{% load static %}
<script src="{% static 'chooseDown.js' %}"></script> {# (1) #}
<script>chooseDown("{{idx}}")</script>
```

1. I'd have preferred to use hyperscript here but it because too unwieldy so settled with some vanilla js and just used hyperscript in the template. Also, this is not yet feature complete. See concepts discussed

[`chooseDown.js`](./dropdown.md) handles dropdown events: mouseover, _mouseclick_, _touchstart_, _keyboard_ press of arrow, escape, tab keys. It's responsible for toggling visibility of the `<ul>` and emitting a `userHasChosen` event to be handled separately by the adopting template.

The adopting templates used here feature:

1. `down-list.html` - hides (but still uses) a real `<select>` field in the DOM, displaying a styleable alternative. Here the `<ul>` has a role of `listbox` and each child item the role of `option`.
2. `_nav.html` - `<ul>` has a role of `menu` and each child item the role of `menuitem`.

## Utils

1. [`{% whitespaceless %}`](./utils.md#whitespaceless)
2. [Filtering of Attributes](./utils.md#filter-attributes)
3. [Wrap Icon Processing](./utils.md#wrap-icon)

## Notes

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
