#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file     jpgSorter.py
@date     2023-06-11
@version  1.2
@license  GNU General Public License v3.0
@author   Alejandro Gonzalez Momblan (agelrenorenardo@gmail.com)
@desc     Sorts jpg images in a directory by creation date.
"""

import ntpath
import os.path
import shutil
from time import localtime, mktime, strftime, strptime
from typing import List, Optional, Tuple

import exifread

unknownDateFolderName = "date-unknown"


def getMinimumCreationTime(exif_data: dict) -> str:
    """
    Returns the minimum creation time from the given exif data.

    Args:
        exif_data (dict): The exif data.

    Returns:
        str: The minimum creation time.

    Examples:
        >>> getMinimumCreationTime({"DateTime": "2021:06:11 12:00:00"})
        '2021:06:11 12:00:00'
        >>> getMinimumCreationTime({"Image DateTime": "2021:06:11 12:00:00"})
        '2021:06:11 12:00:00'
        >>> getMinimumCreationTime({"EXIF DateTimeOriginal": "2021:06:11 12:00:00"})
        '2021:06:11 12:00:00'
        >>> getMinimumCreationTime({"EXIF DateTimeDigitized": "2021:06:11 12:00:00"})
        '2021:06:11 12:00:00'
    """
    assert isinstance(exif_data, dict)

    """
    3 different time fields that can be set independently result in 9 if-cases:
      1. when creationTime is set, prefer it over the others
      2. dateTime = None, prefer dateTimeOriginal over dateTimeDigitized
      3. dateTime and dateTimeDigitized = None, then use dateTimeOriginal
      4. dateTime and dateTimeOriginal = None, then use dateTimeDigitized
      5. dateTime, dateTimeOriginal and dateTimeDigitized = None
    """
    creationTime = (
        exif_data.get("DateTime")
        or exif_data.get("Image DateTime")
        or exif_data.get("EXIF DateTimeOriginal")
        or exif_data.get("EXIF DateTimeDigitized")
    )
    return creationTime


def postprocessImage(images: list, imageDirectory: str, fileName: str) -> None:
    """
    Adds the image to the list of images to be sorted.

    Args:
        images (list): The list of images to be sorted.
        imageDirectory (str): The path of the directory containing the image.
        fileName (str): The name of the image file.

    Examples:
        >>> postprocessImage([], "C:\\Users\\User\\Desktop\\folder", "image.jpg")
    """
    imagePath = os.path.join(imageDirectory, fileName)
    try:
        with open(imagePath, "rb") as image:
            exifTags = exifread.process_file(image, details=False)
            creationTime = getMinimumCreationTime(exifTags)
    except Exception:
        print("Invalid exif tags for " + fileName)
        creationTime = None

    # distinct different time types
    if creationTime is None:
        creationTime = localtime(os.path.getctime(imagePath))
    else:
        try:
            creationTime = strptime(creationTime, "%Y:%m:%d %H:%M:%S")
        except Exception:
            creationTime = localtime(os.path.getctime(imagePath))

    images.append((mktime(creationTime), imagePath))


def createPath(newPath: str) -> None:
    """
    Create a directory path recursively if it doesn't already exist.

    Args:
        newPath (str): The directory path to create.
    """
    os.makedirs(newPath, exist_ok=True)


def createNewFolder(
    destinationRoot: str, year: str, month: Optional[str], eventNumber: int
) -> None:
    """
    Creates a new folder in the destination root based on the specified year,
    month, and event number.

    Args:
        destinationRoot (str): The root directory where the new folder will
            be created.
        year (str): The year of the event.
        month (str or None): The month of the event. Pass None to create
            'year/eventNumber' directories instead of 'year/month/eventNumber'.
        eventNumber (int): The event number.

    Example:
        >>> createNewFolder("/path/to/destination", "2023", "06", 1)
    """
    newPath = (
        os.path.join(destinationRoot, year, month, str(eventNumber))
        if month
        else os.path.join(destinationRoot, year, str(eventNumber))
    )

    createPath(newPath)


def createUnknownDateFolder(destinationRoot: str) -> None:
    """
    Creates a folder with an unknown date in the destination root.

    Args:
        destinationRoot (str): The root directory where the unknown date
            folder will be created.

    Example:
        >>> createUnknownDateFolder("/path/to/destination")
    """
    path = os.path.join(destinationRoot, unknownDateFolderName)
    createPath(path)


def writeImages(
    images: List[Tuple[float, str]],
    destinationRoot: str,
    minEventDeltaDays: int,
    splitByMonth: bool = False,
) -> None:
    """
    Writes the images to the appropriate destination folders based on their
    creation dates.

    Args:
        images (List[Tuple[float, str]]): The list of image tuples containing
            creation time and file path.
        destinationRoot (str): The root directory where the images will be
            written.
        minEventDeltaDays (int): The minimum event delta in days.
        splitByMonth (bool, optional): Whether to split the destination
            folders by month. Default is False.

    Example:
        >>> images = [
        >>>     (1623384000.0, "/path/to/image1.jpg"),
        >>>     (1623470400.0, "/path/to/image2.jpg"),
        >>> ]
        >>> writeImages(images, "/path/to/destination", 7, splitByMonth=True)
    """
    minEventDelta = minEventDeltaDays * 60 * 60 * 24  # convert in seconds
    sortedImages = sorted(images)
    previousTime = None
    eventNumber = 0
    previousDestination = None
    today = strftime("%d/%m/%Y")

    for imageTuple in sortedImages:
        destination = ""
        destinationFilePath = ""
        t = localtime(imageTuple[0])
        year = strftime("%Y", t)
        month = strftime("%m", t) if splitByMonth else None
        creationDate = strftime("%d/%m/%Y", t)
        fileName = ntpath.basename(imageTuple[1])

        if creationDate == today:
            # Create a folder for images with an unknown date
            createUnknownDateFolder(destinationRoot)
            destination = os.path.join(destinationRoot, unknownDateFolderName)
            destinationFilePath = os.path.join(destination, fileName)

        else:
            if (
                previousTime is None
                or (previousTime + minEventDelta) < imageTuple[0]
            ):
                # If the time difference exceeds the minimum event delta, create a new folder
                eventNumber += 1
                createNewFolder(destinationRoot, year, month, eventNumber)

            previousTime = imageTuple[0]

            destComponents = [destinationRoot, year, month, str(eventNumber)]
            destComponents = [v for v in destComponents if v is not None]
            destination = os.path.join(*destComponents)

            if not os.path.exists(destination):
                # If the destination folder does not exist, fallback to the previous destination
                destination = previousDestination

            previousDestination = destination
            destinationFilePath = os.path.join(destination, fileName)

        if not os.path.exists(destinationFilePath):
            # Move the image to the destination folder
            shutil.move(imageTuple[1], destination)
        else:
            if os.path.exists(imageTuple[1]):
                # Remove the image if it already exists in the destination folder
                os.remove(imageTuple[1])


def postprocessImages(
    imageDirectory: str, minEventDeltaDays: int, splitByMonth: bool
) -> None:
    """
    Post-processes the images in the specified directory by organizing them
    into destination folders.

    Args:
        imageDirectory (str): The directory containing the images.
        minEventDeltaDays (int): The minimum event delta in days.
        splitByMonth (bool): Whether to split the destination folders by month.

    Example:
        >>> postprocessImages("/path/to/images", 7, splitByMonth=True)
    """
    images = []
    for root, dirs, files in os.walk(imageDirectory):
        for file in files:
            postprocessImage(images, imageDirectory, file)

    writeImages(images, imageDirectory, minEventDeltaDays, splitByMonth)
