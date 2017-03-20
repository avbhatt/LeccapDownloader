# leccap_dl

An automated lecture recording downloader designed to work with https://leccap.engin.umich.edu.

This implementation downloads selected lectures for a given course into a given directory.

Requires Google Chrome, python3, and Selenium (`$ pip install selenium`).

## Setup

1. Download the most recent version ChromeDriver for your operating system from https://sites.google.com/a/chromium.org/chromedriver/downloads
2. Extract the ChromeDriver zip and move the binary into the same directory as leccap_dl.py

## Usage

`python leccap_dl.py -i [--course-uid] COURSE_UID -o [--output] OUTPUT_DIRECTORY -t [--threaded]`

**Name** | **Type** | **Description**
--- | --- | ---
`--course-uid COURSE_UID` | string | **Optional.** The unique course identifier, which can be found at the end of the leccap URL. Note that this is not the same as the unique identifier for an individual lecture recording. This allows for quick downloads if the course uid is known. If not, a menu of classes will appear.
`--output OUTPUT_DIRECTORY` | string | **Optional.** The directory to output downloaded files to. Defaults to current directory.
`--threaded`| flag | **Optional.** Runs each download in a separate thread. Minimal performance increase, no progress bar.

#### Example
`python leccap_dl.py`
`python leccap_dl.py --course-uid n3yotibeo2l5zofckkx -o /home/user/videos -t`
