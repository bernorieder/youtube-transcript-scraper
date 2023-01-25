# modify these values
filename = 'videos.csv'                                           # filname with video ids
colname = 'contentDetails_videoId'                                # column storing video ids
publishedcolname = 'contentDetails_videoPublishedAt'              # column storing video upload time
delimiter = ','                                                   # delimiter, e.g. ',' for CSV or '\t' for TAB
waittime = 10                                                     # seconds browser waits before giving up
sleeptime = [5,15]                                                # random seconds range before loading next video id
headless = False                                                  # select True if you want the browser window to be invisible (but not inaudible)

# To enable AdBlock, it should be already installed on your Chorme nrowser
# Fetch the `Profile Path` from chrome://version and then find the extentions folder
# The AdBlock extention key is `cfhdojbkjhnklbpkdaibdccddilifddb`
# Add the version installed on your machine
# The overall path should look like this `/home/<USER>/.config/google-chrome/Default/Extensions/cfhdojbkjhnklbpkdaibdccddilifddb/<VERSION>/`
adblock_path = None

#do not modify below
from time import sleep
import csv
import json
import random
import os.path

from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def storecaptions(writefilename, captions=""):
    file = open(writefilename,"w")
    file.write(captions)
    file.close() 

def gettranscript(driver, videoid, publishedAt):
    # check if transcript file already exists
    filekey = "_".join([publishedAt, videoid]) if publishedAt else videoid
    writefilename = 'captions/transcript_%s.txt' % filekey
    if os.path.isfile(writefilename):
        msg = 'transcript file already exists'
        return msg

    # navigate to video
    driver.get("https://www.youtube.com/watch?v=%s&vq=small" % videoid)

    try:
        element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.CLASS_NAME, "ytp-subtitles-button")))
    except:
        msg = 'could not find subtitles button'
        return msg

    # save an empty file if this video has no subtitles, so we don't revisit it if the script is run again
    if "unavailable" in element.get_attribute("title"):
        msg = 'video has no captions'
        storecaptions(writefilename)
        return msg

    # enable subtitles
    try:
        element.click()
    except:
        msg = 'could not click'
        return msg

    # wait for the subtitles to be fetched
    try: 
        request = driver.wait_for_request('/timedtext', timeout=15)
        captionsResp = request.response
        captions = ""
        if captionsResp:
            print("FOUND")
            if captionsResp.status_code >= 200 and captionsResp.status_code < 300:
                content = decode(captionsResp.body, captionsResp.headers.get('Content-Encoding', 'identity'))
                captions = json.dumps(json.loads(content), sort_keys=True, indent=4)
                storecaptions(writefilename, captions)
            else:
                print("Returned with error")
    except:
        msg = 'no captions'
        return msg

    # cool down
    sleep(random.uniform(sleeptime[0],sleeptime[1]))

    # clear all requests
    del driver.requests

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

#create driver
options = Options()

if adblock_path:
    options.add_argument('load-extension=' + adblock_path)

if headless:
    options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

# track only youtube requests
driver.scopes = [
    '.*youtube.*',
]

if adblock_path:
    #let adblock installation finish
    sleep(10)
    #switch back to main tab
    driver.switch_to.window(driver.window_handles[0])

try: 
    for row in csvreader:
        videoId = row[colname]
        publishedOn = row[publishedcolname] if publishedcolname in row else None
        msg = gettranscript(driver, videoId, publishedOn)
        logit(row[colname],msg)
        rowcount -= 1
        print(str(rowcount) + " :  " + row[colname] + " : " + msg)
finally: 
    driver.quit()