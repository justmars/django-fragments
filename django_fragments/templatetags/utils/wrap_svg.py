from bs4 import BeautifulSoup

from .filter_attrs import filter_attrs


def wrap_svg(html_markup: str, css: str | None = None, **kwargs) -> BeautifulSoup:
    """Supplement html fragment of `<svg>` icon with css classes and attributes, include parent/sibling `<span>`s when parameters dictate.

    The following kwargs: `pre_`, `post_`, and `parent_` args are respected.

    So `pre_text` + `pre_class` will add:

    ```html
     <!-- pre_ implies before the icon, with special rule for pre_text -->
    <span class='the-value-of-pre_class'>the-value-of-pre_text</span><svg></svg>
    ```

    `post_text` + `post_class` will add:

    ```html
    <!-- post_ implies after the icon, with special rule for post_text -->
    <svg></svg><span class='the-value-of-post_class'>the-value-of-post_text</span>
    ```

    `parent_class`  + `parent_title` will add:

    ```html
     <!-- parent_ implies a wrapper over the icon,
     'parent_text' will not have same effect.
     -->
    <span class='the-value-of-parent_class' title='the-value-of-parent_title'><svg></svg></span>
    ```

    Examples:
        >>> markup = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5"><path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" /></svg>'
        >>> res = wrap_svg(html_markup=markup, pre_text="Close menu", pre_class="sr-only", aria_hidden="true")
        >>> len(res.contents) == 2
        True
        >>> res.contents[0]
        <span class="sr-only">Close menu</span>
        >>> res.contents[1].attrs == {'xmlns': 'http://www.w3.org/2000/svg', 'viewbox': '0 0 20 20', 'fill': 'currentColor', 'class': ['w-5', 'h-5'], 'aria-hidden': 'true'}
        True
        >>> parented = wrap_svg(html_markup=markup, parent_tag="button", pre_text="Close menu", pre_class="sr-only", aria_hidden="true")
        >>> elements = list(parented.children)
        >>> elements[0].name == 'button'
        True
        >>> list(elements[0].children)
        [<span class="sr-only">Close menu</span>, <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"></path></svg>]

    Args:
        html_markup (str): The template that contains the `<svg>` tag converted into its html string format.
        css (str, optional): Previously defined CSS to add to the `<svg>` icon. Defaults to None.

    Returns:
        SafeString: Small HTML fragment visually representing an svg icon.
    """  # noqa: E501

    soup = BeautifulSoup(html_markup, "html.parser")
    icon = soup("svg")[0]
    if css:
        icon["class"] = css
    if aria_attrs := filter_attrs("aria", kwargs):
        for k, v in aria_attrs.items():
            icon[k] = v

    parent_tag = None
    if tagname := kwargs.pop("parent_tag", None):
        if tagname in ["button", "a", "span", "div"]:
            parent_tag = soup.new_tag(tagname)

    if parent_attrs := filter_attrs("parent", kwargs, unprefix=True):
        if not parent_tag:
            parent_tag = soup.new_tag("span")
        for k, v in parent_attrs.items():
            parent_tag[k] = v
    if parent_tag:
        icon.wrap(parent_tag)

    if left := kwargs.pop("pre_text", None):  # <span>, left of <svg>
        pre_span = soup.new_tag("span")
        pre_span.string = left
        if pre_attrs := filter_attrs("pre", kwargs, unprefix=True):
            for k, v in pre_attrs.items():
                pre_span[k] = v
        icon.insert_before(pre_span)
    elif right := kwargs.pop("post_text", None):  # <span>, right of <svg>
        post_span = soup.new_tag("span")
        post_span.string = right
        if post_attrs := filter_attrs("post", kwargs, unprefix=True):
            for k, v in post_attrs.items():
                post_span[k] = v
        icon.insert_after(post_span)
    return soup
