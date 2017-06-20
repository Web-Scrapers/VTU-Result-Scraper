# Author : Aditya Agarwal
# Script to scrape results declared by VTU

import json
from bs4 import BeautifulSoup
import urllib.request
import os,sys
import time
import re

import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
	def signal_handler(signum, frame):
		raise TimeoutException
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(seconds)
	try:
		yield
	finally:
		signal.alarm(0)

ProviURL	= "http://results.vtu.ac.in/results/result_page.php?usn={0}"
RevalURL	= "http://results.vtu.ac.in/reval_results/result_page.php?usn={0}"
OUTFILE		= "../output/PES2017SemVProvi.csv"
outfile 	= open(OUTFILE,'w')

# Checking existenc of the required directory 
def ckdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

def get_response(aurl):
	hdr					= {'User-Agent':'Mozilla/5.0'}
	req					= urllib.request.Request(aurl,headers=hdr)
	# response			= urllib.request.urlopen(req)

	while True:
		try: 
			# Waiting 60 seconds to recieve a responser object
			with time_limit(30):
				response			= urllib.request.urlopen(req)
			break
		except Exception:
			print("Error opening url!!")
			continue


	return response

# Procedure to return a parseable BeautifulSoup object of a given url
def get_soup(aurl):
	# print(aurl)
	response 			= get_response(aurl)
	soup 				= BeautifulSoup(response,'html.parser')
	return soup


def scrape_reval(USN):
	studentName	= ''

	# url 		= RevalURL.format(USN)
	url 		= ProviURL.format(USN)
	soup		= get_soup(url)
	body		= soup.find("div",{"class":"panel-body"})
	sections	= body.find_all("div")

	try:
		bio			= sections[0].find_all('td')
	except IndexError:
		# print(USN+",No result found")
		return
	studentName	= bio[3].get_text().split(' ',1)[1]

	result 		= sections[2]

	resSummary 	= result.find_all('table')[1].find_all('td')
	SemTot		= resSummary[1].get_text().split(' ',1)[1]
	Result 		= resSummary[3].get_text().split(' ',1)[1]

	outfile.write(USN+','+studentName+','+SemTot+','+Result+'\n')
	# print(USN+','+studentName+','+SemTot+','+Result)

def begin():
	# Write a function to process USNs
	# request page for each USN
	for i in range(0,3):
		for j in range(0,10):
			for k in range(0,10):
				usn = "1PE14CS"+str(i)+str(j)+str(k)
				print("Accessing USN : "+usn)
				scrape_reval(usn)
	# Store the data

if __name__ == "__main__":
	begin()
	outfile.close()
	print("Done")