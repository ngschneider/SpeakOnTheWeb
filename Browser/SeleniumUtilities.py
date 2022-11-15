from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


PATH = "C:\\Users\\Nolan Schneider\\Downloads\\chromedriver_win32 (1)\chromedriver"
URL = "https://Google.com"

# ONLY CHROME for now
def openBrowswer():
    global driver
    driver = webdriver.Chrome(PATH)

def getSite():
    return driver.current_url

def selectElement(elementName, ElementType):
    global currentElement
    match ElementType:
        case "ID":
            currentElement = driver.find_element(By.ID, elementName)
        case "NAME":
            currentElement = driver.find_element(By.NAME, elementName)
        case 'CLASS':
            currentElement = driver.find_element(By.CLASS_NAME, elementName)
            
def sendKeys(text:str):
    currentElement.send_keys(text)
    
def clickButton():
    currentElement.click()
    
def openSite(URL):
    driver.get(URL)
    
    
def refreshPage():
    driver.refresh
    
def navBack():
    driver.back()

def getWebDriver():
    return driver

