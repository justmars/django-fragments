from django.contrib.sites.shortcuts import get_current_site
from django.http.request import HttpRequest
from django.utils.html import format_html

from .fragments import register
from .helpers import strip_whitespace


@register.simple_tag
def og_title(text: str, request: HttpRequest | None = None):
    """Appends site name to end of title, if site name is available."""
    if request and (site := get_current_site(request)):
        if site.name not in text:
            text = f"{text} - {site.name}"
    return format_html(
        strip_whitespace("""
            <title>{text}</title>
            <meta property="og:title" content="{text}"/>
            <meta name="twitter:title" content="{text}"/>
            """),
        text=text,
    )


@register.simple_tag
def og_desc(text: str):
    """Appends description to open graph fields found in description template."""
    return format_html(
        strip_whitespace("""
            <meta name="description" content="{text}"/>
            <meta property="og:description" content="{text}"/>
            <meta name="twitter:description" content="{text}"/>
            """),
        text=text,
    )


@register.simple_tag
def og_img(url: str, alt: str):
    """Appends image details to open graph fields found in image template."""
    return format_html(
        strip_whitespace("""
            <meta property="og:image" content="{url}"/>
            <meta property="og:image:alt" content="{img_alt}"/>
            <meta name="twitter:image" content="{url}"/>
            <meta name="twitter:image:alt" content="{img_alt}"/>
            """),
        url=url,
        img_alt=alt,
    )
