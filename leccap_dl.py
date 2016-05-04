#!/usr/bin/python

import argparse
import urllib
import getpass
from selenium import webdriver

FILE_EXT = ".mp4"

LOGIN_URL = "https://weblogin.umich.edu/"
LECCAP_BASE_URL = "https://leccap.engin.umich.edu/leccap/viewer/s/"

def parse_args():
    parser = argparse.ArgumentParser(\
        description="An automated leccap recording downloader",\
        epilog="example: python leccap_dl.py hsfrlzcioe7xc71tu1w eecs482_lecture")
    parser.add_argument("course_uid",\
        help="the unique leccap course identifier")
    parser.add_argument("file_prefix",\
        help="the file prefix for downloaded lecture recordings")

    return parser.parse_args()

def main():
    args = parse_args()

    uniqname = raw_input("Uniqname: ")
    password = getpass.getpass("Password: ")

    # initialize browser
    browser = webdriver.Chrome(executable_path = './chromedriver')
    browser.implicitly_wait(60) # seconds

    # attempt login
    browser.get(LOGIN_URL)
    browser.find_element_by_id("login").send_keys(uniqname)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_id("loginSubmit").click()

    # go to course leccap page
    leccap_course_url = LECCAP_BASE_URL + args.course_uid
    browser.get(leccap_course_url)

    # scrape lecture urls
    lecture_urls = []
    for rec_btn in browser.find_elements_by_class_name("recording-button"):
        lec_url = rec_btn.get_attribute("href")
        lecture_urls.append(lec_url)

    # scrape video urls from lectures
    video_urls = []
    for lec_url in lecture_urls:
        browser.get(lec_url)

        vid_url = browser.find_element_by_tag_name("video").get_attribute("src")
        video_urls.append(vid_url)

    browser.quit()

    # download videos
    for i in range(len(video_urls)):
        filename = args.file_prefix + str(i + 1) + FILE_EXT

        print("downloading " + filename + " from " + video_urls[i])
        urllib.urlretrieve(video_urls[i], filename)

if __name__ == '__main__':
    main()
