from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


PATH = "C:\\Users\\Nolan Schneider\\Downloads\\chromedriver_win32 (1)\chromedriver"
URL = "https://Google.com"

# ONLY CHROME for now
def openBrowswer():
    global driver
    driver = webdriver.Chrome(PATH)


def openSite(URL):
    driver.get(URL)
    
    
def refreshPage():
    driver.refresh
    
def navBack():
    driver.back()

def getWebDriver():
    return driver

