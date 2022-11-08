### PROCEDURE TO LOGIN FROM A FORM ###

userElmementName= 'UnoUserName'
passElementName= ''

username = ''
password = ''

def findUserElementName():
    pass

def findPassordElementName():
    pass

def findLoginElements():
    pass

def setUsername(user):
    username = user

def setpassword(mypass):
    password = mypass
    
# Ask the user what their username is
def getUsername():
    pass

# Ask the user what their username is
def getpassword():
    pass

def login():
    # Enter username
    driver.find_element(By.ID, userElmementName)
    driver.send_keys(username)
    # Enter password
    driver.find_element(By.ID, passElementName)
    driver.send_keys(password)
    # Submit form
    driver.find_element(By.ID, "submit")