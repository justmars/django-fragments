import re

from django import template
from django.utils.functional import keep_lazy_text

from .fragments import register


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
