"""Main module for the photorec_sort package."""

from argparse import Namespace

from core_helpers.logs import logger
from rich import print  # type: ignore
from rich.traceback import install  # type: ignore

from photorec_sort.cli import get_parsed_args
from photorec_sort.consts import LOG_FILE, PACKAGE
from photorec_sort.jpg_sorter import postprocessImages
from photorec_sort.limit import limitFilesPerFolder
from photorec_sort.utils import (getNumberOfFilesInFolderRecursively,
                                 prepareDirectories, processFiles)


def main() -> None:
    args: Namespace = get_parsed_args()
    install(show_locals=args.debug)
    logger.setup_logger(PACKAGE, LOG_FILE, args.debug, args.verbose)

    source: str = args.source
    destination: str = args.destination
    splitMonths: bool = args.split_months
    keepFilename: bool = args.keep_filename
    date_time_filename: bool = args.date_time_filename
    maxNumberOfFilesPerFolder: int = args.max_per_dir
    minEventDeltaDays: int = args.min_event_delta

    logger.info("Starting recovery...")

    print(
        "Reading from source '%s', writing to destination '%s' (max %i files "
        "per directory, splitting by year %s)."
        % (
            source,
            destination,
            maxNumberOfFilesPerFolder,
            splitMonths and "and month" or "only",
        )
    )
    if keepFilename:
        print("I will keep you filenames as they are")
    elif date_time_filename:
        print(
            "If possible I will rename your files like <Date>_<Time>.jpg - "
            "otherwise keep the filenames as they are"
        )
    else:
        print("I will rename your files like '1.jpg'")

    source, destination = prepareDirectories(source, destination)

    totalAmountToCopy: int = getNumberOfFilesInFolderRecursively(source)
    print("Files to copy:", totalAmountToCopy)

    processFiles(
        source=source,
        destination=destination,
        totalAmountToCopy=totalAmountToCopy,
        keepFilename=keepFilename,
        date_time_filename=date_time_filename,
    )

    logger.info("start special file treatment")
    postprocessImages(destination, minEventDeltaDays, splitMonths)

    logger.info("assure max file per folder number")
    limitFilesPerFolder(destination, maxNumberOfFilesPerFolder)

    logger.info("Finished recovery.")


if __name__ == "__main__":
    main()
