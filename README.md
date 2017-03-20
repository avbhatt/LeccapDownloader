# leccap_dl

An automated lecture recording downloader designed to work with https://leccap.engin.umich.edu.

This implementation downloads selected lectures for a given course into a given directory.

Requires Google Chrome/Firefox/Edge/Safari, python3, and Selenium (`$ pip install selenium`).

## Setup

1. Download the most recent Web Driver for your browser and operating system
    * ChromeDriver: https://sites.google.com/a/chromium.org/chromedriver/downloads
    * FirefoxDriver (Marionette): https://github.com/mozilla/geckodriver/releases
    * Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ [Will **NOT** work unless source code is modified]
    * Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/ [Will **NOT** work unless source code is modified]
2. Extract the WebDriver zip and add the binary into your path
    * Alternatively, just put the binary (chromedriver or geckodriver) in the same folder as leccap_dl.py
    * Or, specify location to chromedriver or geckodriver using `-wdc` or `-wdf` respectively

## Usage
`python leccap_dl.py`
`python leccap_dl.py [-h] [-t] [-i COURSE_UID] [-o OUTPUT_DIRECTORY] [-wdf WEB_DRIVER_FIREFOX] [-wdc WEB_DRIVER_CHROME]`

**Name** | **Type** | **Description**
--- | --- | ---
`--threaded`| flag | **Optional.** Runs each download in a separate thread. Minimal performance increase, no progress bar.
`-i [--course-uid] COURSE_UID` | string | **Optional.** The unique course identifier, which can be found at the end of the leccap URL. Note that this is not the same as the unique identifier for an individual lecture recording. This allows for quick downloads if the course uid is known. If not, a menu of classes will appear.
`-o [--output] OUTPUT_DIRECTORY` | string | **Optional.** The directory to output downloaded files to. Defaults to current directory.
`-wdf [--web-driver-firefox] WEB_DRIVER_FIREFOX` | string | **Optional.** The location of the geckodriver. Defaults to PATH then current directory if not provided.
`-wdc [--web-driver-chrome] WEB_DRIVER_CHROME` | string | **Optional.** The location of the chromedriver. Defaults to PATH then current directory if not provided.



#### Example
`python leccap_dl.py`
`python leccap_dl.py -t --course-uid n3yotibeo2l5zofckkx -o /home/user/videos -wdf /usr/local/bin/geckodriver`
`python leccap_dl.py -o /home/user/videos -wdc /usr/local/bin/chromedriver`
