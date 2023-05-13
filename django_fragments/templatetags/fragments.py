from pathlib import Path

from django import template
from django.conf import settings
from django.forms import BoundField
from django.http.request import HttpRequest
from django.template import Context, Template
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeText, mark_safe
from markdown import markdown

from .utils import filter_attrs, wrap_svg

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
        SafeText: Small HTML fragment visually representing an svg icon but which may contain related tags.
    """  # noqa: E501
    path = folder / f"{prefix}_{name}.html"
    html = render_to_string(str(path))
    svg_with_kwargs = wrap_svg(html_markup=html, css=css, **kwargs)
    return mark_safe(str(svg_with_kwargs).strip())


@register.simple_tag
def toggle_icons(
    btn_kls: str | None = "theme-toggler",
    aria_label: str | None = "Toggle mode",
    **kwargs,
) -> SafeText:
    """Toggle icons. Returns an HTML fragment implementing two `{% icon %}`'s surrounded by a single button which,
    when clicked, implements the toggleTheme() functionality from `doTheme.js`

    Args:
        btn_kls (str | None, optional): _description_. Defaults to "theme-toggler".
        aria_label (str | None, optional): _description_. Defaults to "Toggle mode".

    Returns:
        SafeText: HTML fragment button
    """
    return mark_safe(
        Template("""
            {% load fragments %}
            {% whitespaceless %}
            <button onclick=toggleTheme() type="button" class="{{ btn_kls }}" aria-label="{{aria_label}}">
                {{ icon1 }}
                {{ icon2 }}
            </button>
            {% endwhitespaceless %}
            """)  # noqa: E501
        .render(
            context=Context(
                {
                    "btn_kls": btn_kls,
                    "aria_label": aria_label,
                    "icon1": icon(**filter_attrs(key="icon1", d=kwargs, unprefix=True)),
                    "icon2": icon(**filter_attrs(key="icon2", d=kwargs, unprefix=True)),
                },
            )
        )
        .strip()
    )


@register.simple_tag
def themer(
    btn_kls: str | None = "theme-toggler",
    aria_label: str | None = "Toggle dark mode",
    icon1_name: str | None = "sun",
    icon1_css: str | None = "sun_css",
    icon1_parent_class: str | None = "icon1_svg",
    icon1_pre_text: str | None = "Light mode",
    icon1_pre_class: str | None = "sr-only",
    icon2_name: str | None = "moon",
    icon2_css: str | None = "moon_css",
    icon2_parent_class: str | None = "icon2_svg",
    icon2_pre_text: str | None = "Dark mode",
    icon2_pre_class: str | None = "sr-only",
    **kwargs,
) -> SafeText:
    """A wrapper over `toggle_icons()` but specific to a toggle for the common sun and moon
    pattern.

    Each icon uses the same signature as {% icon %}. To apply a value to the first icon,
    use the prefix `icon_1`. To apply a value to the second icon, use the prefix `icon_2`. If
    none are supplied, icon_1 will contain defaults for 'sun', icon_2 will contain defaults
    for 'moon'.

    So with `tog(icon_1_name='sun', icon_2_Name='moon')`, would implement the equivalent of
    2 {% icon %} template tags surrounded by a button, e.g.:

    ```jinja
    <button>
        {% icon name='sun' %}
        {% icon name='moon' %}
    </button>
    ```

    This implies that the svgs for `sun` and `moon` are present in the designated template folder.

    Args:
        btn_kls (str | None, optional): Will populate the button's `class` attribute.. Defaults to "theme-toggler".
        aria_label (str | None, optional): Will populate the button's `aria-label` attribute. Defaults to "Toggle mode".
        icon1_name (str | None, optional): Will be used to create first {% icon %}. Defaults to "sun".
        icon1_css (str | None, optional): Will be used to create first {% icon %}. Defaults to "sun_css".
        icon1_parent_class (str | None, optional): Will be used to create first {% icon %}. Defaults to "icon1_svg".
        icon1_pre_text (str | None, optional): Will be used to create first {% icon %}. Defaults to "Light mode".
        icon1_pre_class (str | None, optional): Will be used to create first {% icon %}. Defaults to "sr-only".
        icon2_name (str | None, optional): Will be used to create second {% icon %}. Defaults to "moon".
        icon2_css (str | None, optional): Will be used to create second {% icon %}. Defaults to "moon_css".
        icon2_parent_class (str | None, optional): Will be used to create second {% icon %}. Defaults to "icon2_svg".
        icon2_pre_text (str | None, optional): Will be used to create second {% icon %}. Defaults to "Dark mode".
        icon2_pre_class (str | None, optional): Will be used to create second {% icon %}. Defaults to "sr-only".

    Returns:
        SafeText: HTML fragment button
    """
    return toggle_icons(
        btn_kls=btn_kls,
        aria_label=aria_label,
        **(
            dict(
                icon1_name=icon1_name,
                icon1_css=icon1_css,
                icon1_parent_class=icon1_parent_class,
                icon1_pre_text=icon1_pre_text,
                icon1_pre_class=icon1_pre_class,
                icon2_name=icon2_name,
                icon2_css=icon2_css,
                icon2_parent_class=icon2_parent_class,
                icon2_pre_text=icon2_pre_text,
                icon2_pre_class=icon2_pre_class,
            )
            | kwargs
        ),
    )


@register.simple_tag
def hput(
    bound: BoundField,
    kls: str | None = "h",
    label_kls: str | None = None,
    validate: str | None = None,
) -> SafeText:
    """An encapsulation of an idiomatic BoundField with an optional ability for htmx inline
    field validation if a url is passed as `validate` argument.

    Args:
        bound (BoundField): The field to render
        kls (str | None, optional): If supplied will supply the containing div's class attribute. Defaults to "h".
        label_kls (str | None, optional): If supplied will supply the containing div's class attribute. Defaults to None.
        validate (str | None, optional): A url that should be the form's submit url for inline field validation using htmx. Defaults to None.

    Returns:
        SafeText: The html fragment consisting of a wrapped field
    """  # noqa: E501
    from .helpers import hx_enable_inline_validation

    if not isinstance(bound, BoundField):
        raise Exception(f"Improper field {bound=}")

    attrs = hx_enable_inline_validation(bound, validate) if validate else ""
    return mark_safe(
        Template("""
            {% load fragments %}
            {% whitespaceless %}
            <div {{attrs}}
                {% if bound.is_hidden %}hidden{% endif %}
                {% if bound.errors %}data-invalid=true{% endif %}
                class="{{ kls }}"
                data-widget="{{ bound.widget_type }}"
            >
                <label for="{{ bound.id_for_label }}"
                    {% if label_kls %}class="{{ label_kls }}"{% endif %}>
                    {{bound.label}}
                </label>
                {{ bound }}
                <small>{{ bound.help_text }}</small>
                {{ bound.errors }}
            </div>
            {% endwhitespaceless %}
            """)  # noqa: E501
        .render(
            context=Context(
                {
                    "bound": bound,
                    "label_kls": label_kls,
                    "kls": kls,
                    "attrs": attrs,
                },
            )
        )
        .strip()
    )
