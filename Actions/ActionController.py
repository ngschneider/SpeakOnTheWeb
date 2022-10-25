### MAIN file ###
### ATTEMPTS TO RECOGNIZE THE INTENDED ACTION OF THE USER ###

# POSSIBLE ACTIONS THE WEB BROWSER COULD DO
from asyncio.windows_events import NULL


actions = ["LOGIN", "SEARCH", "REFRESH", "Back", ""]

# DICTIONARY OF RELATED WORDS TO A PARTICULAR ACTION
keyWords = {
    'LOGIN' : ['login','sign in', 'username', 'password'],
    'SEARCH' : ['search', 'look up' , 'go to'],
    'REFRESH' : ['refresh', 'reload'],
    'BACK' : ['go back', 'back']
}

## CREATE FUNCTION THAT IS A INCOMING STREAM OF TEXT from the microphone
def incomingWordStream():
    pass

## Decides what the intended user action is
def deductIntendedAction():
    pass

while(True):
    text = incomingWordStream
    if text != NULL:
        intendedAction = deductIntendedAction
        
        if intendedAction == 'LOGIN':
            ## LOGIN 
            pass
        elif intendedAction == 'SEARCH':
            ## SEARCH
            pass
        elif intendedAction == 'BACK':
            ## BACK
            pass
    
