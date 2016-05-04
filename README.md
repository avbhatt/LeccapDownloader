# leccap_dl

An automated lecture recording downloader designed to work with https://leccap.engin.umich.edu.

This implementation downloads all lectures for a given course into the current working directory.

Requires Google Chrome and Selenium (`$ pip install selenium`).

## Setup

1. Download the most recent version ChromeDriver for your operating system from https://sites.google.com/a/chromium.org/chromedriver/downloads
2. Extract the ChromeDriver zip and move the binary into the same directory as leccap_dl.py

## Usage

`python leccap_dl.py course_uid file_prefix`

**Name** | **Type** | **Description**
--- | --- | ---
`course_uid` | string | **Required.** The unique course identifier, which can be found at the end of the leccap URL. Note that this is not the same as the unique identifier for an individual lecture recording.
`file_prefix` | string | **Required.** The filename prefix. Lecture recordings are saved as the prefix followed by an integer.

#### Example

`python leccap_dl.py hsfrlzcioe7xc71tu1w eecs482_lecture`
