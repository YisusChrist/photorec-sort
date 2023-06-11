<p align="center">
    <a href="https://github.com/yisuschrist/sort-PhotorecRecoveredFiles/issues">
        <img src="https://img.shields.io/github/issues/yisuschrist/sort-PhotorecRecoveredFiles?color=171b20&label=Issues%20%20&logo=gnubash&labelColor=e05f65&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/yisuschrist/sort-PhotorecRecoveredFiles/forks">
        <img src="https://img.shields.io/github/forks/yisuschrist/sort-PhotorecRecoveredFiles?color=171b20&label=Forks%20%20&logo=git&labelColor=f1cf8a&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/yisuschrist/sort-PhotorecRecoveredFiles/">
        <img src="https://img.shields.io/github/stars/yisuschrist/sort-PhotorecRecoveredFiles?color=171b20&label=Stargazers&logo=octicon-star&labelColor=70a5eb">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/yisuschrist/sort-PhotorecRecoveredFiles/pulls">
        <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/yisuschrist/sort-PhotorecRecoveredFiles?color=0088ff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://opensource.org/license/gpl-3-0/">
        <img alt="License" src="https://img.shields.io/github/license/yisuschrist/sort-PhotorecRecoveredFiles?color=0088ff">
    </a>
    <!--
    <a href="https://github.com/yisuschrist/sort-PhotorecRecoveredFiles/issues/contributors">
        <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/yisuschrist/sort-PhotorecRecoveredFiles" />
    </a>
    -->
</p>

<br>

<p align="center">
    <a href="https://github.com/yisuschrist/sort-PhotorecRecoveredFiles/issues/new/choose">Report Bug</a>
    ·
    <a href="https://github.com/yisuschrist/sort-PhotorecRecoveredFiles/issues/new/choose">Request Feature</a>
    ·
    <a href="https://github.com/yisuschrist/sort-PhotorecRecoveredFiles/discussions">Ask Question</a>
    ·
    <a href="https://github.com/yisuschrist/sort-PhotorecRecoveredFiles/security/policy#reporting-a-vulnerability">Report security bug</a>
</p>

<br>

Photorec does a great job when recovering deleted files. But the result is a huge, unsorted, unnamed amount of files. Especially for external hard drives serving as backup of all the personal data, sorting them is an endless job.

This program sPRF helps you sorting your files. First of all, the **files are copied to own folders for each file type**. Second, **jpgs are distinguished by the year, and optionally by month as well** when they have been taken **and by the event**. We thereby define an event as a time span during them photos are taken. It has a delta of 4 days without a photo to another event. If no date from the past can be detected, these jpgs are put into one folder to be sorted manually.

## Installation

First install the package [exifread](https://pypi.python.org/pypi/ExifRead):

```bash
pip install exifread
```

## Run the sorter

Then run the sorter:

```bash
python recovery.py <path to files recovered by Photorec> <destination>
```

This copies the recovered files to their file type folder in the destination directory. The recovered files are not modified. If a file already exists in the destination directory, it is skipped. This means that the program can be interrupted with Ctrl+C and then continued at a later point by running it again.

The first output of the program is the number of files to copy. To count them might take some minutes depending on the amount of recovered files. Afterwards you get some feedback on the processed files.

### Parameters

For an overview of all arguments, run with the `-h` option:

```bash
python recovery.py -h
```

#### Max numbers of files per folder

All directories contain a maximum of 500 files by default. If there are more for a file type, numbered subdirectories are created. If you want another file-limit, e.g. 1000, pass that number as the third parameter when running the program:

```bash
python recovery.py <path to files recovered by Photorec> <destination> -n1000
```

#### Folder for each month

sPRF usually sorts your photos by year:

```
destination
|- 2015
  |- 1.jpg
  |- 2.jpg
  |- ...
|- 2016
  |- ...
```

Sometimes you might want to sort each year by month. This can be done using the `-m` parameter:

```bash
python recovery.py <path to files recovered by Photorec> <destination> -m
```

Now you get:

```
destination
|- 2015
  |- 1
    |- 1.jpg
    |- 2.jpg
  |- 2
    |- 3.jpg
    |- 4.jpg
  |- ...
|- 2016
  |- ...
```

#### Keep original filenames

Use the `-k` parameter to keep the original filenames:

```bash
python recovery.py <path to files recovered by Photorec> <destination> -k
```

#### Adjust event distance

For the case you want to reduce or increase the timespan between events, simply use the parameter `-d`. The default is 4:

```bash
python recovery.py <path to files recovered by Photorec> <destination> -d10
```

#### Rename jpg-files with `<Date>_<Time>` from EXIF data if possible

If the original jpg image files were named by `<Date>_<Time>` it might be useful to rename the recovered files in the same way. This can be done by adding the parameter `-j`.

```bash
python recovery.py <path to files recovered by Photorec> <destination> -j
```

If no EXIF data can be retrieved the original filename is kept.

In case there are two or more files with the same EXIF data the filename is extended by an index to avoid overwriting files.

The result will look like:

```
20210121_134407.jpg
20210122_145205.jpg
20210122_145205(1).jpg
20210122_145205(2).jpg
20210122_145813.jpg
20210122_153155.jpg
```
