"""Constants for the photorec_sort package."""

from pathlib import Path

from core_helpers.xdg_paths import get_user_path

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata  # type: ignore

__version__: str = metadata.version(__package__ or __name__)
__desc__: str = metadata.metadata(__package__ or __name__)["Summary"]
GITHUB: str = metadata.metadata(__package__ or __name__)["Home-page"]
PACKAGE: str = metadata.metadata(__package__ or __name__)["Name"]

LOG_PATH: Path = get_user_path(PACKAGE, "log")
LOG_FILE: Path = LOG_PATH / f"{PACKAGE}.log"

DEBUG = False
