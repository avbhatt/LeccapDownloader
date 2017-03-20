#!/usr/bin/python3

import argparse
import requests
from clint.textui import progress
import getpass
from selenium import webdriver
import threading
import re
import sys

FILE_EXT = ".mp4"

LOGIN_URL = "https://weblogin.umich.edu/"
LECCAP = "https://leccap.engin.umich.edu/leccap"
LECCAP_BASE_URL = LECCAP + "/viewer/s/"

def parse_args():
	parser = argparse.ArgumentParser(\
		description="An automated leccap recording downloader",\
		epilog="example: python leccap_dl.py hsfrlzcioe7xc71tu1w [-o /home/user/videos] [-t]")
	parser.add_argument("-i","--course-uid",\
		help="the unique leccap course identifier")
	parser.add_argument("-o", "--output-directory",\
		default='.',\
		help="directory to output files (default: current directory [.])")
	parser.add_argument("-t", "--threaded",\
		help="if used, each download will be put in a new thread",\
		action="store_true")
	parser.add_argument("-wdf", "--web-driver-firefox",\
		help="specify location of firefox WebDriver if not in current directory or PATH")
	parser.add_argument("-wdc", "--web-driver-chrome",\
		help="specify location of chrome WebDriver if not in current directory or PATH")

	return parser.parse_args()

def main():
	args = parse_args()

	uniqname = input("Uniqname: ")
	password = getpass.getpass("Password: ")

	# initialize browser
	if args.web_driver_chrome:
		try:
			browser = webdriver.Chrome(args.web_driver_chrome)
		except Exception:
			try:
				browser = webdriver.Chrome()
			except Exception:
				try:
					browser = webdriver.Firefox()
				except Exception:
					if sys.platform == 'win32':
						try:
							browser = webdriver.Chrome('./chromedriver.exe')
						except Exception:
							try:
								browser = webdriver.Firefox(executable_path='./geckodriver.exe')
							except:
								print("Please add Chrome/Firefox WebDriver to path or current directory", file=sys.stderr)
								exit(1)
					else:
						try:
							browser = webdriver.Chrome('./chromedriver')
						except Exception:
							try:
								browser = webdriver.Firefox(executable_path='./geckodriver')
							except:
								print("Please add Chrome/Firefox WebDriver to path or current directory", file=sys.stderr)
								exit(1)
	elif args.web_driver_firefox:
		try:
			browser = webdriver.Firefox(executable_path=args.web_driver_firefox)
		except Exception:
			try:
				browser = webdriver.Chrome()
			except Exception:
				try:
					browser = webdriver.Firefox()
				except Exception:
					if sys.platform == 'win32':
						try:
							browser = webdriver.Chrome('./chromedriver.exe')
						except Exception:
							try:
								browser = webdriver.Firefox(executable_path='./geckodriver.exe')
							except:
								print("Please add Chrome/Firefox WebDriver to path or current directory", file=sys.stderr)
								exit(1)
					else:
						try:
							browser = webdriver.Chrome('./chromedriver')
						except Exception:
							try:
								browser = webdriver.Firefox(executable_path='./geckodriver')
							except:
								print("Please add Chrome/Firefox WebDriver to path or current directory", file=sys.stderr)
								exit(1)
	else:	
		try:
			browser = webdriver.Chrome()
		except Exception:
			try:
				browser = webdriver.Firefox()
			except Exception:
				if sys.platform == 'win32':
					try:
						browser = webdriver.Chrome('./chromedriver.exe')
					except Exception:
						try:
							browser = webdriver.Firefox(executable_path='./geckodriver.exe')
						except:
							print("Please add Chrome/Firefox WebDriver to path or current directory", file=sys.stderr)
							exit(1)
				else:
					try:
						browser = webdriver.Chrome('./chromedriver')
					except Exception:
						try:
							browser = webdriver.Firefox(executable_path='./geckodriver')
						except:
							print("Please add Chrome/Firefox WebDriver to path or current directory", file=sys.stderr)
							exit(1)

	browser.implicitly_wait(60) # seconds

	# attempt login
	browser.get(LOGIN_URL)
	browser.find_element_by_id("login").send_keys(uniqname)
	browser.find_element_by_id("password").send_keys(password)
	browser.find_element_by_id("loginSubmit").click()

	if args.course_uid:
		# go to course leccap page
		leccap_course_url = LECCAP_BASE_URL + args.course_uid
		browser.get(leccap_course_url)
	else:
		# find available courses
		browser.get(LECCAP)
		i = 0
		class_uid = []
		for classes in browser.find_elements_by_class_name("list-group-item"):
			class_uid.append(classes.get_attribute("href").split("/")[-1])
			print("[%d] Class: %s" % (i, classes.text))
			i += 1
		class_index = input("Select class: ")
		leccap_course_url = LECCAP_BASE_URL + class_uid[int(class_index)]
		browser.get(leccap_course_url)
	
	# scrape lecture urls
	lecture_urls = []
	lecture_names = []
	i = 0
	for rec_btn in browser.find_elements_by_class_name("recording-button"):
		lec_url = rec_btn.get_attribute("href")
		lecture_urls.append(lec_url)
		for rec_info in rec_btn.find_elements_by_class_name("recording-info"):
			date = rec_info.find_element_by_class_name("recording-date").text
			name = rec_info.find_element_by_class_name("recording-title").text
			lecture_names.append(name)
			print("[%d] Name: %s \t Date: %s" % (i, name, date))
		i += 1
	true_urls = []
	print("Select video(s) to download (space delimited). * to download all")
	select_indices = [x if x == '*' else int(x) for x in input().split()]
	if select_indices[0] == '*':
		true_urls = [(lecture_urls[i], lecture_names[i]) for i in range(len(lecture_urls))]
	else:
		true_urls = [(lecture_urls[i], lecture_names[i]) for i in select_indices]
	video_urls = []
	for (lec_url, useless) in true_urls:
		browser.get(lec_url)
		vid_url = browser.find_element_by_tag_name("video").get_attribute("src")
		video_urls.append(vid_url)

	browser.quit()

	output_directory = args.output_directory
	if output_directory[-1] == '/':
		output_directory = output_directory[:-1]

	# download videos
	threads = []
	for i in range(len(video_urls)):
		lec_name = true_urls[i][1]
		lec_name = re.sub('[;/?:"=|*]','-',lec_name)
		filename =  output_directory + '/' + lec_name + FILE_EXT
		if args.threaded:
			threads.append(threading.Thread(target=download_file, args=(filename, video_urls[i])))
		else:
			print("downloading " + filename + " from " + video_urls[i])
			r = requests.get(video_urls[i], stream=True)
			with open(filename, 'wb') as f:
				total_length = int(r.headers.get('content-length'))
				for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
					if chunk:
						f.write(chunk)
	if args.threaded:
		for i in threads:
			i.start()

def download_file(filename, url):
	print("downloading " + filename + " from " + url)
	r = requests.get(url, stream=True)
	f = open(filename, 'wb')
	for chunk in r.iter_content(chunk_size=1024):
		if chunk:
			f.write(chunk)
	f.close()

if __name__ == '__main__':
	main()
