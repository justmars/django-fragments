# Install


```py title="pip install django-fragments, add to settings.py"
INSTALLED_APPS = [
    "django_fragments", # add this
]
FRAGMENTS = {
    "icons_prefix": "heroicons", # prefix to use, see {% icons %} for details
    "icons_path": BASE_DIR / "templates" / "xxx" # type: Path, where svg stored
}
```
