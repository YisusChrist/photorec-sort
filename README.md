<p align="center">
    <a href="https://github.com/YisusChrist/photorec-sort/issues">
        <img src="https://img.shields.io/github/issues/YisusChrist/photorec-sort?color=171b20&label=Issues%20%20&logo=gnubash&labelColor=e05f65&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/photorec-sort/forks">
        <img src="https://img.shields.io/github/forks/YisusChrist/photorec-sort?color=171b20&label=Forks%20%20&logo=git&labelColor=f1cf8a&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/photorec-sort/stargazers">
        <img src="https://img.shields.io/github/stars/YisusChrist/photorec-sort?color=171b20&label=Stargazers&logo=octicon-star&labelColor=70a5eb">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/yisuschrist/urls_organizer/actions">
        <img alt="Tests Passing" src="https://github.com/YisusChrist/photorec-sort/actions/workflows/github-code-scanning/codeql/badge.svg">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/photorec-sort/pulls">
        <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/YisusChrist/photorec-sort?color=0088ff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://opensource.org/license/unlicense">
        <img alt="License" src="https://img.shields.io/github/license/YisusChrist/photorec-sort?color=0088ff">
    </a>
</p>

<br>

<p align="center">
    <a href="https://github.com/YisusChrist/photorec-sort/issues/new?assignees=YisusChrist&labels=bug&projects=&template=bug_report.yml">Report Bug</a>
    ·
    <a href="https://github.com/YisusChrist/photorec-sort/issues/new?assignees=YisusChrist&labels=feature&projects=&template=feature_request.yml">Request Feature</a>
    ·
    <a href="https://github.com/YisusChrist/photorec-sort/issues/new?assignees=YisusChrist&labels=question&projects=&template=question.yml">Ask Question</a>
    ·
    <a href="https://github.com/YisusChrist/photorec-sort/security/policy#reporting-a-vulnerability">Report security bug</a>
</p>

<br>

![Alt](https://repobeats.axiom.co/api/embed/bf002b17544124f48536d107b2acff75fcc77396.svg "Repobeats analytics image")

<br>

Photorec does a great job when recovering deleted files. But the result is a huge, unsorted, unnamed amount of files. Especially for external hard drives serving as backup of all the personal data, sorting them is an endless job.

This program sPRF helps you sorting your files. First of all, the **files are copied to own folders for each file type**. Second, **jpgs are distinguished by the year, and optionally by month as well** when they have been taken **and by the event**. We thereby define an event as a time span during them photos are taken. It has a delta of 4 days without a photo to another event. If no date from the past can be detected, these jpgs are put into one folder to be sorted manually.

<details>
<summary>Table of Contents</summary>

- [Requirements](#requirements)
- [Installation](#installation)
  - [From PyPI](#from-pypi)
  - [Manual installation](#manual-installation)
  - [Uninstall](#uninstall)
- [Usage](#usage)
  - [Parameters](#parameters)
    - [Max numbers of files per folder](#max-numbers-of-files-per-folder)
    - [Folder for each month](#folder-for-each-month)
    - [Keep original filenames](#keep-original-filenames)
    - [Adjust event distance](#adjust-event-distance)
    - [Rename jpg-files with `<Date>_<Time>` from EXIF data if possible](#rename-jpg-files-with-date_time-from-exif-data-if-possible)
- [TODO](#todo)
- [License](#license)
- [Credits](#credits)

</details>

## Requirements

Here's a breakdown of the packages needed and their versions:

- [poetry](https://pypi.org/project/poetry) >= 1.8.3 (_only for manual installation_)
- [core-helpers](https://github.com/YisusChrist/core_helpers)
- [exifread](https://pypi.org/project/ExifRead) >= 3.0.0
- [rich](https://pypi.org/project/rich) >= 13.5.3

> [!NOTE]
> The software has been developed and tested using Python `3.12.1`. The minimum required version to run the software is Python 3.9. Although the software may work with previous versions, it is not guaranteed.

## Installation

### From PyPI

`photorec_sort` can be installed easily as a PyPI package. Just run the following command:

```bash
pip3 install photorec_sort
```

> [!IMPORTANT]
> For best practices and to avoid potential conflicts with your global Python environment, it is strongly recommended to install this program within a virtual environment. Avoid using the --user option for global installations. We highly recommend using [pipx](https://pypi.org/project/pipx) for a safe and isolated installation experience. Therefore, the appropriate command to install `photorec_sort` would be:
>
> ```bash
> pipx install photorec_sort
> ```

The program can now be ran from a terminal with the `photorec_sort` command.

### Manual installation

If you prefer to install the program manually, follow these steps:

> [!WARNING]
> This will install the version from the latest commit, not the latest release.

1. Download the latest version of [photorec_sort](https://github.com/YisusChrist/photorec-sort) from this repository:

   ```bash
   git clone https://github.com/YisusChrist/photorec-sort
   cd photorec_sort
   ```

2. Install the package:

   ```bash
   poetry install --only main
   ```

3. Run the program:

   ```bash
   poetry run photorec_sort
   ```

### Uninstall

If you installed it from PyPI, you can use the following command:

```bash
pipx uninstall photorec_sort
```

## Usage

Then run the sorter:

```bash
photorec_sort <path to files recovered by Photorec> <destination>
```

This copies the recovered files to their file type folder in the destination directory. The recovered files are not modified. If a file already exists in the destination directory, it is skipped. This means that the program can be interrupted with Ctrl+C and then continued at a later point by running it again.

The first output of the program is the number of files to copy. To count them might take some minutes depending on the amount of recovered files. Afterwards you get some feedback on the processed files.

### Parameters

> [!TIP]
> For more information about the usage of the program, run `photorec_sort --help` or `photorec_sort -h`.

![usage](https://i.imgur.com/K0kVMXq.png)

#### Max numbers of files per folder

All directories contain a maximum of 500 files by default. If there are more for a file type, numbered subdirectories are created. If you want another file-limit, e.g. 1000, pass that number as the third parameter when running the program:

```bash
photorec_sort <path to files recovered by Photorec> <destination> -n1000
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
photorec_sort <path to files recovered by Photorec> <destination> -m
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
photorec_sort <path to files recovered by Photorec> <destination> -k
```

#### Adjust event distance

For the case you want to reduce or increase the timespan between events, simply use the parameter `-d`. The default is 4:

```bash
photorec_sort <path to files recovered by Photorec> <destination> -d10
```

#### Rename jpg-files with `<Date>_<Time>` from EXIF data if possible

If the original jpg image files were named by `<Date>_<Time>` it might be useful to rename the recovered files in the same way. This can be done by adding the parameter `-j`.

```bash
photorec_sort <path to files recovered by Photorec> <destination> -j
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

## TODO

Planing to add the following features:

- [x] Reorganize and beautify the Readme adding sections
- [ ] Add a full documentation in Wiki section
- [ ] Add a Changelog / Release Notes

## License

`photorec_sort` is released under the [Unlicense License](https://opensource.org/license/unlicense).

## Credits

This is a forked version from the original project [sort-PhotorecRecoveredFiles](https://github.com/tfrdidi/sort-PhotorecRecoveredFiles).
