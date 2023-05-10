import os
import sys
from pathlib import Path

import django


def prep_nb(base_dir_path: Path = Path().cwd()):
    sys.path.insert(0, str(base_dir_path))
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings"
    )  # Access django imports
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = (
        "true"  # Allow qs async filtering in a cell
    )
    django.setup()  # This is for setting up django
