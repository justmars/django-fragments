# django-fragments

![Github CI](https://github.com/justmars/django-fragments/actions/workflows/main.yml/badge.svg)

## Purpose

Used for partial template rendering of: `<input>`, `<svg>` tags. Originally for a Django [boilerplate](https://start-django.fly.dev), refactored out into an independent library.

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

See [documentation](https://justmars.github.io/django-fragments).
