from argparse import (ArgumentParser, ArgumentTypeError, Namespace,
                      RawTextHelpFormatter)

from .consts import PACKAGE
from .consts import __version__ as VERSION


def check_valid_int(value: str) -> int:
    ivalue = int(value)
    if ivalue < 1:
        raise ArgumentTypeError(
            "Max number of files per directory must be at least 1, but %s was introduced"
            % value
        )
    return ivalue


def get_parsed_args() -> Namespace:
    """
    Get parsed arguments

    Returns:
        argparse.Namespace: The parsed arguments.

    Example:
    >>> get_parsed_args()
    Namespace(key="value")
    """
    description = """\
Sort files recovered by Photorec.
The input files are first copied to the destination, sorted by file type.
Then JPG files are sorted based on creation year (and optionally month).
Finally any directories containing more than a maximum number of files are
accordingly split into separate directories.
"""

    parser = ArgumentParser(
        description=description,
        formatter_class=RawTextHelpFormatter,  # Disable line wrapping
        allow_abbrev=False,  # Disable abbreviations
        add_help=False,  # Disable default help
    )

    # Main arguments
    main_group = parser.add_argument_group("Main Arguments")
    main_group.add_argument(
        "-src",
        "--source",
        metavar="path",
        type=str,
        # required=True,
        help="source directory with files recovered by Photorec",
    )
    main_group.add_argument(
        "-dst",
        "--destination",
        metavar="path",
        type=str,
        # required=True,
        help="destination directory to write sorted files to",
    )

    # Sorting options
    sorting_group = parser.add_argument_group("Sorting Options")
    sorting_group.add_argument(
        "-n",
        "--max-per-dir",
        metavar="N",
        type=check_valid_int,
        default=500,
        help="maximum number of files per directory",
    )
    sorting_group.add_argument(
        "-m",
        "--split-months",
        action="store_true",
        default=False,
        help="split JPEG files not only by year but by month as well",
    )
    sorting_group.add_argument(
        "-k",
        "--keep_filename",
        action="store_true",
        default=True,
        help="keeps the original filenames when copying",
    )

    # Miscellaneous options
    misc_group = parser.add_argument_group("Miscellaneous Options")
    misc_group.add_argument(
        "-md",
        "--min-event-delta",
        metavar="DAYS",
        type=int,
        default=4,
        help="minimum delta in days between two days",
    )
    misc_group.add_argument(
        "-j",
        "--date_time_filename",
        action="store_true",
        default=False,
        help="sets the filename to the exif date and time if possible - "
        "otherwise keep the original filename",
    )

    # Help and information
    info_group = parser.add_argument_group("Information")
    info_group.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit."
    )
    info_group.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Show log messages on screen. Default is False.",
    )
    info_group.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Activate debug logs. Default is False.",
    )
    info_group.add_argument(
        "-V",
        "--version",
        action="version",
        help="Show version number and exit.",
        version=f"{PACKAGE} version {VERSION}",
    )

    return parser.parse_args()
