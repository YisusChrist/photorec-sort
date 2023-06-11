#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file     numberOfFilesPerFolderLimiter.py
@date     2023-06-11
@version  1.2
@license  GNU General Public License v3.0
@author   Alejandro Gonzalez Momblan (agelrenorenardo@gmail.com)
@desc     Limits the number of files per folder in a directory.
"""

import os
import shutil


def distributeFilesIntoSubfolders(
    dirPath: str, maxNumberOfFilesPerFolder: int
) -> None:
    """
    Distributes files into subfolders based on the maximum number of files per
    folder.

    Args:
        dirPath (str): The path of the directory.
        maxNumberOfFilesPerFolder (int): The maximum number of files per
            folder.
    """
    numberOfSubfolders = (
        len(os.listdir(dirPath)) - 1
    ) // maxNumberOfFilesPerFolder + 1
    createSubfolders(dirPath, numberOfSubfolders)
    moveFilesToSubfolders(dirPath, maxNumberOfFilesPerFolder)


def createSubfolders(dirPath: str, numberOfSubfolders: int) -> None:
    """
    Creates subfolders in the directory.

    Args:
        dirPath (str): The path of the directory.
        numberOfSubfolders (int): The number of subfolders to create.
    """
    for subFolderNumber in range(1, numberOfSubfolders + 1):
        subFolderPath = os.path.join(dirPath, str(subFolderNumber))
        os.makedirs(subFolderPath, exist_ok=True)


def moveFilesToSubfolders(
    dirPath: str, maxNumberOfFilesPerFolder: int
) -> None:
    """
    Moves files to the appropriate subfolders based on the maximum number of
    files per folder.

    Args:
        dirPath (str): The path of the directory.
        maxNumberOfFilesPerFolder (int): The maximum number of files per
            folder.
    """
    fileCounter = 1
    for file in sorted(os.listdir(dirPath)):
        source = os.path.join(dirPath, file)
        if os.path.isfile(source):
            destDir = str((fileCounter - 1) // maxNumberOfFilesPerFolder + 1)
            destination = os.path.join(dirPath, destDir, file)
            shutil.move(source, destination)
            fileCounter += 1


def limitFilesPerFolder(folder: str, maxNumberOfFilesPerFolder: int) -> None:
    """
    Limits the number of files per folder in a directory.

    Args:
        folder (str): The path of the folder to limit.
        maxNumberOfFilesPerFolder (int): The maximum number of files per
            folder.

    Raises:
        ValueError: If the folder does not exist.
        ValueError: If the maxNumberOfFilesPerFolder is not a positive integer.

    Examples:
        >>> limitFilesPerFolder("C:\\Users\\User\\Desktop\\folder", 100)
    """
    if not os.path.exists(folder):
        raise ValueError("The folder does not exist.")
    if maxNumberOfFilesPerFolder <= 0:
        raise ValueError(
            "The maxNumberOfFilesPerFolder is not a positive integer."
        )

    # Iterate through directories and subdirectories in reverse order
    for root, dirs, files in os.walk(folder, topdown=False):
        for directory in dirs:
            dirPath = os.path.join(root, directory)
            filesInFolder = len(os.listdir(dirPath))

            if filesInFolder > maxNumberOfFilesPerFolder:
                distributeFilesIntoSubfolders(
                    dirPath, maxNumberOfFilesPerFolder
                )

    # TODO: Add multiprocessing using Pool().map