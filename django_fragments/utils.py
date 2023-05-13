import os
import sys
from pathlib import Path

import django
from django.http.request import HttpRequest


def is_htmx(request: HttpRequest) -> bool:
    """Determines whether or not the request should be handled differently
    because of the presence of the `HTTP_HX_REQUEST` header.

    Args:
        request (HttpRequest): The Django request object received from the view

    Returns:
        bool: Whether or not `HTTP_HX_REQUEST` exists.
    """
    return True if request.META.get("HTTP_HX_REQUEST") else False


def prep_nb(base_dir_path: Path = Path().cwd()):
    sys.path.insert(0, str(base_dir_path))
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings"
    )  # Access django imports
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = (
        "true"  # Allow qs async filtering in a cell
    )
    django.setup()  # This is for setting up django
