import os
from argparse import Namespace

from rich import print  # type: ignore

from .cli import get_parsed_args
from .jpg_sorter import postprocessImages
from .limit import limitFilesPerFolder
from .logs import logger
from .utils import (getNumberOfFilesInFolderRecursively, prepareDirectories,
                    processFiles)


def main() -> None:
    args: Namespace = get_parsed_args()

    source: str = args.source
    destination: str = args.destination
    splitMonths: bool = args.split_months
    keepFilename: bool = args.keep_filename
    date_time_filename: bool = args.date_time_filename
    maxNumberOfFilesPerFolder: int = args.max_per_dir
    minEventDeltaDays = args.min_event_delta

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
