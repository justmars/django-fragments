from pathlib import Path

from django import template
from django.conf import settings
from django.forms import Field
from django.http.request import HttpRequest
from django.template import Context, Template
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeText, mark_safe
from markdown import markdown

from .utils import wrap_svg

register = template.Library()


@register.filter
def md(text: str, exts: list[str] = ["attr_list"]) -> SafeText:
    """Convert a text in markdown to its html equivalent using specific extensions."""
    return mark_safe(markdown(text, extensions=exts))


@register.simple_tag
def curr(lhs: str, reversible: str) -> SafeText:
    """Returns a string `aria-current` for use as an attribute when `lhs` path matches the
    `reversible` value that will be passed to the `django.urls.reverse()`.

    Args:
        lhs (str): lhs stands for lefthand side, should be first positional element in the tag
        reversible (str): The value will be passed to the `django.urls.reverse()` without args, kwargs

    Returns:
        SafeText: The text "aria-current=page" if a match occurs, otherwise ""
    """  # noqa: E501
    return mark_safe("aria-current=page" if lhs == reverse(reversible) else "")


@register.simple_tag
def nava(
    reversible: str,
    text: str | None = None,
    css: str | None = None,
    request: HttpRequest | None = None,
) -> SafeText:
    """HTML fragment: `<a>` tag for desktop/mobile navbar links.

    Checks if link represented by reverse name url `reversible` is the _current_ path via the request, if it is provided.

    In the latter case, on match of the `request.path` to the `reversible`, add `aria-current=true`

    Args:
        reversible (str): The value will be passed to the `django.urls.reverse()` function without keyword arguments
        text (str | None, optional): The text to incude within the anchor element, if any. Defaults to None.
        css (str | None, optional): If provided, will populate the `class` attribute of the anchor element. Defaults to None.
        request (HttpRequest | None, optional): The django http request object to ascertain the present path of the request. Defaults to None.

    Returns:
        SafeText: The output anchor tag
    """  # noqa: E501
    return format_html(
        "<a {aria} href='{url}' class='{css}'>{text}</a>",
        text=text or "",
        url=reverse(reversible),
        css=css,
        aria=curr(request.path, reversible) if request else "",
    )


@register.simple_tag
def icon(
    name: str,
    prefix: str = settings.FRAGMENTS.get("icons_prefix"),
    folder: Path = settings.FRAGMENTS.get("icons_path"),
    css: str | None = None,
    **kwargs,
) -> SafeText:
    """Make an `<svg>` fragment, using a file found within the `name` + `prefix` + `folder` path, and add the appropriate
    css classes and attributes, optionally including parent/sibling tags when parameters dictate.

    Args:
        name (str): The prefixless (prefix_) name of the `html` file containing an `<svg>` icon, presumes to be formatted and included in the proper folder previously.
        css (str, optional): Previously defined CSS to add to the `<svg>` icon. Defaults to None.
        prefix (str, optional): Source of the svg file; needs to be declared in `settings.py`.
        folder (str, optional): Where to find the template; needs to be declared in `settings.py`.
        **kwargs (dict): The following kwargs: `pre_`, `post_`, and `parent_` args are respected by `start_html_tag_helpers`

    Returns:
        SafeString: Small HTML fragment visually representing an svg icon but which may contain related tags.
    """  # noqa: E501
    path = folder / f"{prefix}_{name}.html"
    html = render_to_string(str(path))
    svg_with_kwargs = wrap_svg(html_markup=html, css=css, **kwargs)
    return mark_safe(str(svg_with_kwargs).strip())


@register.simple_tag
def input(bound: Field, kls: str, label_kls: str | None = None) -> SafeText:
    """Can likely replace this with prospective Django 5.0's
    `django.forms.BoundField.as_field_group`"""
    return mark_safe(
        Template("""
            {% load fragments %}
            {% whitespaceless %}
            <div class="{{ kls }}
                data-hidden="{{ bound.is_hidden}}"
                data-widget="{{ bound.widget_type }}"
            >
                {{ bound.errors }}
                <label for="{{ bound.id_for_label }}"
                    {% if label_kls %}class="{{ label_kls }}"{% endif %}>
                    {{bound.label}}
                </label>
                {{ bound }}
                <p class="help">{{ bound.help_text }}</p>
            </div>
            {% endwhitespaceless %}
            """)  # noqa: E501
        .render(
            context=Context(
                {
                    "bound": bound,
                    "kls": kls,
                    "label_kls": label_kls,
                },
            )
        )
        .strip()
    )
