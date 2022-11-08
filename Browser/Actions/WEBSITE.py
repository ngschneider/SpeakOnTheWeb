#### TO USE THIS COMMAND :
### Requires a URL ADDRESS to BE FOUND

urlState: bool = False

def findAddress(command: list):
    for x in command:
        ### Find common Top-Level-Domains
        location = -1
        location = x.find(".")
        if(location != -1):
            print("" + x[location:])
            return (True, "" + x)
    
    return (False, "")
        
    
    
def requirment(command: list):
    global urlState
    if(not urlState):
        ### Find url
        return findAddress(command)
     
    
    print()
    