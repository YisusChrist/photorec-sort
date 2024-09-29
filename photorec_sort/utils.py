import os
from pathlib import Path
import shutil
from time import strftime, strptime

import exifread  # type: ignore
from rich.progress import Progress

from .jpg_sorter import getMinimumCreationTime
from .logs import logger

fileCounter: int = 0


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
        logger.info(f"File [{filename}] already exists, renamed to {new_filename}")
        return new_filename
    else:
        # If no file with the same basename exists, return the original filename
        return filename


def moveFile(
    destination: str,
    keepFilename: bool,
    date_time_filename: bool,
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
    global fileCounter

    extension: str = os.path.splitext(file)[1][1:].upper()
    sourcePath: str = os.path.join(root, file)

    destinationDirectory: str = os.path.join(
        destination, extension if extension else "_NO_EXTENSION"
    )

    os.makedirs(destinationDirectory, exist_ok=True)

    if keepFilename:
        fileName: str = file

    elif date_time_filename:
        index = 0
        with open(sourcePath, "rb") as image:
            exifTags = exifread.process_file(image, details=False)

        creationTime = getMinimumCreationTime(exifTags)
        try:
            creationTime = strptime(creationTime, "%Y:%m:%d %H:%M:%S")
            creationTime = strftime("%Y%m%d_%H%M%S", creationTime)
            fileName = f"{creationTime}.{extension.lower()}"
            while os.path.exists(os.path.join(destinationDirectory, fileName)):
                index += 1
                fileName = f"{creationTime}({index}).{extension.lower()}"

        except Exception as e:
            logger.warning(f"Could not get creation time for file [{sourcePath}]")
            fileName = file

    else:
        fileName = str(fileCounter)
        if extension:
            fileName += f".{extension.lower()}"

    destinationFile = os.path.join(destinationDirectory, fileName)
    if not os.path.exists(destinationFile):
        # Check if source directory and destination directory are the same
        if os.path.abspath(root) == os.path.abspath(destination):
            logger.info(f"Moving [{sourcePath}] to [{destinationFile}]")
            shutil.move(sourcePath, destinationFile)
        else:
            logger.info(f"Copying [{sourcePath}] to [{destinationFile}]")
            shutil.copy2(sourcePath, destinationFile)

    fileCounter += 1
    """
    if (fileCounter % onePercentFiles) == 0:
        log(str(fileCounter) + " / " + totalAmountToCopy + " processed.")
    """


def sanitize_path(path: str) -> str:
    """
    Sanitize the path using pathlib, resolving it and ensuring no path traversal.

    Args:
        path (str): The path to sanitize.

    Returns:
        str: The sanitized path.
    """
    # Convert the path to an absolute resolved path
    resolved_path: Path = Path(path).resolve()

    # Ensure the resolved path does not contain any '..' traversal
    if ".." in resolved_path.parts:
        raise ValueError(f"Invalid path: {path}. Potential path traversal detected.")

    return str(resolved_path)


def prompt_for_directory(directory_type: str) -> str:
    """
    Prompt the user for a valid directory input.

    Args:
        directory_type (str): The type of directory.

    Returns:
        str: A valid directory path.
    """
    while True:
        directory: str = input(f"Enter a valid {directory_type} directory: ")
        if os.path.exists(directory):
            return directory
        print(f"Directory '{directory}' does not exist. Please try again.")


def prepareDirectories(source: str, destination: str) -> tuple[str, str]:
    """
    Prepare the source and destination directories.

    Args:
        source (str): The source directory.
        destination (str): The destination directory.

    Returns:
        tuple: The source and destination directories.
    """
    source = (
        sanitize_path(prompt_for_directory("source"))
        if not source
        else sanitize_path(source)
    )
    destination = (
        sanitize_path(prompt_for_directory("destination"))
        if not destination
        else sanitize_path(destination)
    )

    return source, destination


def processFiles(
    source: str,
    destination: str,
    totalAmountToCopy: int,
    keepFilename: bool,
    date_time_filename: bool,
) -> None:
    """
    Process files in a source directory.

    Args:
        source (str): The source directory.
        destination (str): The destination directory.
        totalAmountToCopy (int): The total number of files to copy.
        keepFilename (bool): Whether to keep the original filename.
        date_time_filename (bool): Whether to set the filename to the exif date and time if possible.

    Examples:
        >>> processFiles("source", "destination", "totalAmountToCopy", False, False)
        0 / totalAmountToCopy processed.

        >>> processFiles("source", "destination", "totalAmountToCopy", True, True)
        0 / totalAmountToCopy processed.
    """
    global fileCounter

    with Progress() as progress:
        task = progress.add_task("Processing files...", total=totalAmountToCopy)

        for root, dirs, files in os.walk(source, topdown=False):
            for file in files:
                try:
                    moveFile(
                        destination=destination,
                        keepFilename=keepFilename,
                        date_time_filename=date_time_filename,
                        root=root,
                        file=file,
                    )
                    progress.update(task, advance=1)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error("Exception (%s)", e)
                    continue

    logger.info(f"{fileCounter} / {totalAmountToCopy} processed.")
