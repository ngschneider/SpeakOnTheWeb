from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import SeleniumUtilities as selUtil
import time

## LOCATION OF WEB DRIVER
PATH = "C:\\Users\\Nolan Schneider\\Downloads\\chromedriver_win32 (1)\chromedriver"
URL = "https://Google.com"
selUtil.openBrowswer()
selUtil.openSite(URL)
selUtil.refreshPage()
selUtil.openSite("https://Twitter.com")
time.sleep(60)
selUtil.navBack()

#assert "Python" in driver.title
#elem = driver.find_element(By.NAME, "q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
#driver.close()