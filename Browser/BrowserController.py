### MAIN file ###

import Browser.SeleniumUtilities as selUtil
import Browser.Actions.WEBSITE as website
import Browser.Actions.SEARCH as search


### ATTEMPTS TO RECOGNIZE THE INTENDED ACTION OF THE USER ###

# POSSIBLE ACTIONS THE WEB BROWSER COULD DO

browserOpenState: bool = False

actions = ["LOGIN", "SEARCH", "REFRESH", "Back", "OPEN"]

# DICTIONARY OF RELATED WORDS TO A PARTICULAR ACTION
keyWords = {
    "login" : "LOGIN",
    "sign in" : "LOGIN",
    "reload" : "REFRESH",
    "refresh" : "REFRESH",
    "search" : "SEARCH",
    "website" : "WEBSITE",
    "site" : "WEBSITE",
    "go to" : "WEBSITE",
    "back" : "BACK",
    'pause' : 'PAUSE',
    'play' : "PAUSE"
}


## Decides what the intended user action is
def deductIntendedAction(command: list):
    for x in command:
        return keyWords.get(x)
    
    return ""
    


def browserAction(command: list): 
    global browserOpenState
    print("Browser Action")
    print(command)
    intendedAction = deductIntendedAction(command)
    print(intendedAction)
    if((not browserOpenState)):
        selUtil.openBrowswer()
        browserOpenState = True
    
    if intendedAction == 'LOGIN':
        ## LOGIN 
         pass
    elif intendedAction == 'PAUSE':
        selUtil.selectElement('ytp-play-button ytp-button', 'CLASS' )
        selUtil.clickButton()
        pass
    elif intendedAction == 'SEARCH':
        
        status = search.requirment(selUtil.getSite(), command)
        print(status)
        if status[0]:
            # SELECT THE TECT BOX & SEND KEY
            selUtil.selectElement(status[2][1],status[2][0])
            selUtil.sendKeys(status[1])
            
            # SELECT THE BUTTON & CLICK
            selUtil.selectElement(status[2][3],status[2][2])
            selUtil.clickButton()
        
    elif intendedAction == 'BACK':
        selUtil.navBack()
        pass
    elif intendedAction == 'REFRESH':
        selUtil.refreshPage()
        pass
    elif intendedAction == 'WEBSITE':
        ## SEARCH FOR A WEBSITE
        status = website.requirment(command)
        if(status[0]):
            selUtil.openSite("https://" + status[1]) 
        else:
            print("FAILED TO GET URL")    
    else:
        print("Did not recognize command")
        
    
