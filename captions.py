import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

videoid = "s7zXV1NT2D8"

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# go to the google home page
driver.get("https://www.youtube.com/watch?v="+videoid)

# the page is ajaxy so the title is originally this:
print(driver.title)

try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "yt-icon-button.dropdown-trigger > button:nth-child(1)")))
except:
	print("problem")
	driver.quit()

element.click()

try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "yt-formatted-string.ytd-menu-service-item-renderer")))
finally:
	print("problem")

element.click()

try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-transcript-body-renderer.style-scope")))
finally:
	print("problem")

print(element.text)

file = open("transcript_"+videoid+".txt","w")
file.write(element.text)
file.close() 

driver.quit()