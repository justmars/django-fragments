# django-fragments

![Github CI](https://github.com/justmars/django-fragments/actions/workflows/main.yml/badge.svg)

## Purpose

Used for partial template rendering of: `<input>`, `<svg>` tags for a Django [boilerplate](https://start-django.fly.dev)

## Setup

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

## Documentation

## `{% load fragments %}`

1. [`{% btn %}`](https://justmars.github.io/django-fragments/btn.md) - translates: `btn_*`, `data_*`, `aria_*`, and [`hx_*`](https://htmx.org)
2. [`{% btn_a %}`](https://justmars.github.io/django-fragments/btn.md) - translates: `btn_*`, `data_*`, `aria_*`, and [`hx_*`](https://htmx.org) - can apply `data_*`, `aria_*` to `<a type='button'>`
3. [`{% icon %}`](https://justmars.github.io/django-fragments/icon.md) - translates: `btn_*`, `data_*`, `aria_*`, and [`hx_*`](https://htmx.org) - idiomatic `<svg>` combiner with neighboring / parent tags
4. [`{% input %}`](https://justmars.github.io/django-fragments/input.md) - translates: `btn_*`, `data_*`, `aria_*`, and [`hx_*`](https://htmx.org) - A limited, simple `<input>`-based `BoundField` + related `<label>`, tags for `help_css`, `label_css` (complements  `django-widget-tweaks`).

## `{% load og %}`

1. `{% og_title %}` - adds title and open graph meta title
2. `{% og_desc %}` - adds meta desc and open graph meta desc / twitter
3. `{% og_img %}`  - adds open graph img / twitter

See [documentation](https://justmars.github.io/django-fragments).
