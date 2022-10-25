from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# ONLY CHROME for now
def openBrowswer(File):
    global driver
    driver = webdriver.Chrome(File)


def openSite(URL):
    driver.get(URL)
    
    
def refreshPage():
    driver.refresh
    
def navBack():
    driver.back()

def getWebDriver():
    return driver

