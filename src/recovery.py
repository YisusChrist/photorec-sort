#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file     recovery.py
@date     2023-06-11
@version  1.1
@license  GNU General Public License v3.0
@author   Alejandro Gonzalez Momblan (agelrenorenardo@gmail.com)
@desc     Sort files recovered by Photorec.
"""

import argparse
import logging
import os
import os.path
import pathlib
import shutil
import sys
from time import localtime, strftime, strptime

import exifread

import jpgSorter
import numberOfFilesPerFolderLimiter

splitMonths = False
source = None
destination = None
keepFilename = False
date_time_filename = False
fileCounter = 0


def get_version():
    """
    Return the version of the program.

    Returns:
        str: The version of the program.
    """
    try:
        # Open the file and read its contents.
        with open(pathlib.Path(__file__)) as f:
            content = f.read()
        return grab(content, "@version", "\n").strip()
    except:
        print("Could not find version")


def grab(text: str, start: str, end: str = "\n") -> str:
    """
    Extract a string between a given start and end string within a larger
    string.

    Author: Julio Cabria (https://github.com/Julynx)

    Args:
        text (str): The larger string to search within.
        start (str): The starting string to search for.
        end (str, optional): The ending string to search for. Defaults to "\n".

    Returns:
        str: The string between the start and end strings, if found.
            Otherwise, an empty string.
    """
    # Find the starting index of the desired substring
    start_index = text.find(start)
    # Find the ending index of the desired substring
    end_index = text.find(end, start_index + len(start))
    # Return the substring between the start and end indices.
    return text[start_index + len(start) : end_index]


def getNumberOfFilesInFolderRecursively(start_path: str = ".") -> int:
    """
    Get the number of files in a folder recursively.

    Args:
        start_path (str, optional): The path to the folder. Defaults to ".".

    Returns:
        int: The number of files in the folder.

    Examples:
        >>> getNumberOfFilesInFolderRecursively()
        0

        >>> getNumberOfFilesInFolderRecursively("path/to/folder")
        10
    """
    numberOfFiles = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                numberOfFiles += 1
    return numberOfFiles


def getNumberOfFilesInFolder(path: str = ".") -> int:
    """
    Get the number of files in a folder.

    Args:
        path (str, optional): The path to the folder. Defaults to ".".

    Returns:
        int: The number of files in the folder.

    Examples:
        >>> getNumberOfFilesInFolder()
        1

        >>> getNumberOfFilesInFolder("path/to/folder")
        10
    """
    return len(os.listdir(path))


def log(logString: str) -> None:
    """
    Log a string to the console.

    Args:
        logString (str): The string to log.

    Examples:
        >>> log("Hello, world!")
        00:00:00: Hello, world!
    """
    print(strftime("%H:%M:%S", localtime()) + ": " + logString)


def renameFileIfExists(filename: str) -> str:
    """
    Rename a file if it already exists.

    Args:
        filename (str): The filename to rename.

    Returns:
        str: The new filename.

    Examples:
        >>> renameFileIfExists("file")
        file

        >>> renameFileIfExists("file")
        file_1
    """
    # Split the filename into basename and extension
    basename, extension = os.path.splitext(filename)
    # Check if a file with the same basename exists in the same directory
    if os.path.isfile(filename):
        # If a file with the same basename exists, add a counter to the basename
        counter = 1
        while os.path.isfile(f"{basename}_{counter}{extension}"):
            counter += 1
        new_filename = f"{basename}_{counter}{extension}"
        # Rename the file with the new filename
        logging.info(
            f"File [{filename}] already exists, renamed to {new_filename}"
        )
        return new_filename
    else:
        # If no file with the same basename exists, return the original filename
        return filename


def moveFile(
    destination: str,
    keepFilename: bool,
    root: str,
    file: str,
) -> None:
    """
    Move a file to a destination directory.

    Args:
        destination (str): The destination directory.
        keepFilename (bool): Whether to keep the original filename.
        root (str): The root directory of the file.
        file (str): The filename.

    Examples:
        >>> move_file("destination", False, "root", "file")
        Moving [root/file] to [destination/0.jpg]

        >>> move_file("destination", True, "root", "file")
        Moving [root/file] to [destination/file]
    """
    global fileCounter, date_time_filename

    extension = os.path.splitext(file)[1][1:].upper()
    sourcePath = os.path.join(root, file)

    if extension:
        destinationDirectory = os.path.join(destination, extension)
    else:
        destinationDirectory = os.path.join(destination, "_NO_EXTENSION")

    if not os.path.exists(destinationDirectory):
        os.mkdir(destinationDirectory)

    if keepFilename:
        fileName = file

    elif date_time_filename:
        index = 0
        with open(sourcePath, "rb") as image:
            exifTags = exifread.process_file(image, details=False)

        creationTime = jpgSorter.getMinimumCreationTime(exifTags)
        try:
            creationTime = strptime(str(creationTime), "%Y:%m:%d %H:%M:%S")
            creationTime = strftime("%Y%m%d_%H%M%S", creationTime)
            fileName = str(creationTime) + "." + extension.lower()
            while os.path.exists(os.path.join(destinationDirectory, fileName)):
                index += 1
                fileName = (
                    str(creationTime)
                    + "("
                    + str(index)
                    + ")"
                    + "."
                    + extension.lower()
                )
        except:
            fileName = file

    else:
        fileName = str(fileCounter)
        if extension:
            fileName += "." + extension.lower()

    destinationFile = os.path.join(destinationDirectory, fileName)
    if not os.path.exists(destinationFile):
        logging.info(f"Moving [{sourcePath}] to [{destinationFile}]")
        shutil.copy2(sourcePath, destinationFile)

    fileCounter += 1
    """
    if (fileCounter % onePercentFiles) == 0:
        log(str(fileCounter) + " / " + totalAmountToCopy + " processed.")
    """


def get_parsed_args() -> argparse.Namespace:
    """
    Get parsed arguments

    Returns:
        argparse.Namespace: The parsed arguments.

    Example:
    >>> get_parsed_args()
    Namespace(key="value")
    """
    global parser

    description = """Sort files recovered by Photorec.
The input files are first copied to the destination, sorted by file type.
Then JPG files are sorted based on creation year (and optionally month).
Finally any directories containing more than a maximum number of files are
accordingly split into separate directories."""

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter,  # Disable line wrapping
        allow_abbrev=False,  # Disable abbreviations
        add_help=False,  # Disable default help
    )

    # Main arguments
    main_group = parser.add_argument_group("Main Arguments")
    main_group.add_argument(
        "source",
        metavar="src",
        type=str,
        help="source directory with files recovered by Photorec",
    )
    main_group.add_argument(
        "destination",
        metavar="dest",
        type=str,
        help="destination directory to write sorted files to",
    )

    # Sorting options
    sorting_group = parser.add_argument_group("Sorting Options")
    sorting_group.add_argument(
        "-n",
        "--max-per-dir",
        type=int,
        default=500,
        required=False,
        help="maximum number of files per directory",
    )
    sorting_group.add_argument(
        "-m",
        "--split-months",
        action="store_true",
        required=False,
        help="split JPEG files not only by year but by month as well",
    )
    sorting_group.add_argument(
        "-k",
        "--keep_filename",
        action="store_true",
        required=False,
        help="keeps the original filenames when copying",
    )

    # Miscellaneous options
    misc_group = parser.add_argument_group("Miscellaneous Options")
    misc_group.add_argument(
        "-md",
        "--min-event-delta",
        type=int,
        default=4,
        required=False,
        help="minimum delta in days between two days",
    )
    misc_group.add_argument(
        "-j",
        "--date_time_filename",
        action="store_true",
        required=False,
        help="sets the filename to the exif date and time if possible - "
        "otherwise keep the original filename",
    )

    # Help and information
    info_group = parser.add_argument_group("Information")
    info_group.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit."
    )
    info_group.add_argument(
        "-t",
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
        "-v",
        "--version",
        action="version",
        help="Show version number and exit.",
        version=f"%(prog)s version {get_version()}",
    )

    return parser.parse_args()


def setup_logger(
    args: argparse.Namespace,
    log_file: str = __file__ + ".log",
) -> None:
    """
    Set up the logger for this instance.

    This method sets up the logger for the instance based on the `verbose`
    and `debug` command line arguments.

    Args:
        - args (argparse.Namespace): The command line arguments.
        - log_file (str): The file to log to. Defaults to __file__ + ".log".

    Example:
    >>> setup_logger(args, "log.txt")
    """
    handlers = [logging.FileHandler(log_file)]
    level = logging.INFO
    msg_format = "[%(asctime)s] %(levelname)s: %(message)s"

    if args.verbose:
        handlers.append(logging.StreamHandler())

    if args.debug:
        level = logging.DEBUG
        msg_format += ": %(pathname)s:%(lineno)d in %(funcName)s"

    logging.basicConfig(
        level=level,
        format=msg_format,
        handlers=handlers,
    )


def main():
    global splitMonths, source, destination, keepFilename, date_time_filename

    args = get_parsed_args()
    setup_logger(args, "recovery.log")

    source = args.source
    destination = args.destination
    maxNumberOfFilesPerFolder = args.max_per_dir
    splitMonths = args.split_months
    keepFilename = args.keep_filename
    date_time_filename = args.date_time_filename
    minEventDeltaDays = args.min_event_delta

    logging.info("Starting recovery...")

    if maxNumberOfFilesPerFolder < 1:
        print("Error: max number of files per directory must be at least 1")
        sys.exit(1)

    print(
        "Reading from source '%s', writing to destination '%s' (max %i files per directory, splitting by year %s)."
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
            "If possible I will rename your files like <Date>_<Time>.jpg - otherwise keep the filenames as they are"
        )
    else:
        print("I will rename your files like '1.jpg'")

    while (source is None) or (not os.path.exists(source)):
        source = input("Enter a valid source directory\n")
    while (destination is None) or (not os.path.exists(destination)):
        destination = input("Enter a valid destination directory\n")

    fileNumber = getNumberOfFilesInFolderRecursively(source)
    onePercentFiles = int(fileNumber / 100) if fileNumber > 100 else fileNumber
    totalAmountToCopy = str(fileNumber)
    print("Files to copy: " + totalAmountToCopy)

    for root, dirs, files in os.walk(source, topdown=False):
        for file in files:
            # TODO: Add tqdm module for progress bar
            try:
                moveFile(destination, keepFilename, root, file)
            except Exception as e:
                logging.error("Exception (%s)", e)
                continue
            except KeyboardInterrupt:
                break

    logging.info(str(fileCounter) + " / " + totalAmountToCopy + " processed.")

    logging.info("start special file treatment")
    jpgSorter.postprocessImages(
        os.path.join(destination, "JPG"), minEventDeltaDays, splitMonths
    )

    logging.info("assure max file per folder number")
    numberOfFilesPerFolderLimiter.limitFilesPerFolder(
        destination, maxNumberOfFilesPerFolder
    )

    logging.info("Finished recovery.")


if __name__ == "__main__":
    main()
