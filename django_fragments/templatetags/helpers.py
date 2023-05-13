import re

from django import template
from django.forms import BoundField
from django.template import Context, Template
from django.utils.functional import keep_lazy_text
from django.utils.safestring import SafeText, mark_safe

from .fragments import register


@register.simple_tag(takes_context=True)
def htmx_csrf(context) -> SafeText:
    """Just a tiny fragment to signify htmx-compatible requests
    that will include the csrf_token."""
    return mark_safe(
        Template("""hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'""").render(
            context=Context(context)
        )
    )


@register.simple_tag
def attrize(d: dict) -> SafeText:
    """Unpack a dictionary as attributes, useful for adding attributes to
    an existing tag."""
    return mark_safe(" ".join([f'{k}="{v}"' for k, v in d.items()]))


def hx_enable_inline_validation(bound: BoundField, url: str) -> str:
    """Given a `BoundField` and a `url`, implement inline field validation proposed by
    [hernantz](https://hernantz.github.io/inline-form-validation-with-django-and-htmx.html).
    It makes use of various tags from [htmx](https://htmx.org).

    The gist: form is prematurely submitted (because of `hx-post`) as an AJAX-request,
    the partial template response will `hx-swap` an `hx-target`. In other words, the
    old field is replaced by the same field... but now as a result of `form.is_valid()`.

    The response, if it contains errors, will include an error list for the field.

    Instead of rendering the entire partial response, the use of `hx-select` limits the
    replacement to a segment of the partial response.

    Args:
        bound (BoundField): A Django field with data previously submitted
        url (str): Where the form is submitted.
    Returns:
        str: A string of text attributes that can be added to a wrapping div of a `BoundField`
    """  # noqa: E501
    idx = f"hput_{bound.id_for_label}"
    return attrize(
        {
            "id": idx,
            "hx-select": f"#{idx}",
            "hx-post": url,
            "hx-trigger": "blur from:find input",
            "hx-target": f"#{idx}",
            "hx-swap": "outerHTML",
        }
    )


@keep_lazy_text
def strip_whitespace(value):
    """
    See https://stackoverflow.com/a/72942459 answer by [Will Gordon](https://stackoverflow.com/users/6758654/will-gordon)
    Return the given HTML with any newlines, duplicate whitespace, or trailing spaces are removed.
    """  # noqa: E501
    # Process duplicate whitespace occurrences or
    # *any* newline occurrences and reduce to a single space
    value = re.sub(r"\s{2,}|[\n]+", " ", str(value))
    # After processing all of the above,
    # any trailing spaces should also be removed
    # Trailing space examples:
    #   - <div >                    Matched by: \s(?=[<>"])
    #   - < div>                    Matched by: (?<=[<>])\s
    #   - <div class="block ">      Matched by: \s(?=[<>"])
    #   - <div class=" block">      Matched by: (?<==\")\s
    #   - <span> text               Matched by: (?<=[<>])\s
    #   - text </span>              Matched by: \s(?=[<>"])
    value = re.sub(r'\s(?=[<>"])|(?<==\")\s|(?<=[<>])\s', "", str(value))
    return value


class WhitespacelessNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return strip_whitespace(self.nodelist.render(context).strip())


@register.tag
def whitespaceless(parser, token):
    """Remove whitespace within HTML tags, including tab, newline and extra space characters. Warning: this affects all text within the `whitespaceless` command without prejudice. Use with caution."""  # noqa: E501
    nodelist = parser.parse(("endwhitespaceless",))
    parser.delete_first_token()
    return WhitespacelessNode(nodelist)
