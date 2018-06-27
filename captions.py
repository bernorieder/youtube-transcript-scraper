# modify these values
filename = 'videolist_zembla_273_2018_05_25-09_17_02.tab'			# filname with video ids
colname = 'videoId'													# column storing video ids
delimiter = '\t'													# delimiter, e.g. ',' for CSV or '\t' for TAB
waittime = 10														# seconds browser waits before giving up
sleeptime = [5,15]													# random seconds range before loading next video id
headless = True														# select True if you want the browser window to be invisible (but not inaudible)

#do not modify below
from time import sleep
import csv
import random
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


def gettranscript(videoid):

	# check if transcript file already exists	
	writefilename = 'subtitles/transcript_' + videoid + '.txt'
	if os.path.isfile(writefilename):
		msg = 'transcript file already exists'
		return msg

	sleep(random.uniform(sleeptime[0],sleeptime[1]))

	options = Options()
	options.add_argument("--headless")

	# Create a new instance of the Firefox driver
	if headless:
		driver = webdriver.Firefox(firefox_options=options)
	else:
		driver = webdriver.Firefox()

	# navigate to video
	driver.get("https://www.youtube.com/watch?v="+videoid)

	try:
	    element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.CSS_SELECTOR, "yt-icon-button.dropdown-trigger > button:nth-child(1)")))
	except:
		msg = 'could not find options button'
		driver.quit()
		return msg

	try:
		element.click()
	except:
		msg = 'could not click'
		driver.quit()
		return msg

	try:
	    element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#items > ytd-menu-service-item-renderer:nth-child(2) > yt-formatted-string"))) #items > ytd-menu-service-item-renderer:nth-child(2) > yt-formatted-string
	except:
		msg = 'could not find transcript in options menu'
		driver.quit()
		return msg

	try:
		element.click()
	except:
		msg = 'could not click'
		driver.quit()
		return msg

	try:
	    element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-transcript-body-renderer.style-scope")))
	except:
		msg = 'could not find transcript text'
		driver.quit()
		return msg

	#print(element.text)

	file = open(writefilename,"w")
	file.write(element.text)
	file.close() 

	driver.quit()

	return 'ok'

# log function
def logit(id,msg):
	logwriter.writerow({'id':id,'msg':msg})
	

# prepare log file
logwrite = open('captions.log','w',newline='\n')
logwriter = csv.DictWriter(logwrite, fieldnames=['id','msg'])
logwriter.writeheader()

# read CSV file
csvread = open(filename, newline='\n')
csvreader = csv.DictReader(csvread, delimiter=delimiter, quoting=csv.QUOTE_NONE)
rowcount = len(open(filename).readlines())

for row in csvreader:
	msg = gettranscript(row[colname])
	logit(row[colname],msg)
	rowcount -= 1
	print(str(rowcount) + " :  " + row[colname] + " : " + msg)