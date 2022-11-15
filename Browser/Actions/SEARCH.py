#### SEARCH REQUIRMENTS ####
### SEARCH IS SITE SPECIFIC, SO THE FORM ELEMENTS NEED TO BE KNOW FOR EACH SITE.

# KEY ARE SITES THAT HAVE BEEN IMPLEMENTED, VALUE IS THE NORMAILZED NAME; example, youtube.com -> youtube
searchableSites = {
    'youtube.com' : 'youtube',
    'youtube' : 'youtube',
    'google' : 'google'
}

# Key is the site to search, Value a truple of the element type and element name
# Should be in the form (TYPE,textbox element, TYPE, ButtonELEMENT)
elementTag = {
    'youtube' : ('NAME', 'search_query', "ID", 'search-icon-legacy'),
    'google' : ('NAME', 'q','NAME', 'btnK' )
}

# FUNCTION TO DETERMINE IF THE SITE BEEN HAS IMPLEMENTED
# RETURNS 
#   Tuple
#       Boolean : True if the site has been implemented
#       String : Name of site 
def isSearchable(site: str):
    if(site in searchableSites):
        return (True,searchableSites.get(site))
    else:
        return (False,"")


# FUNCTION to get string of site with only the name of the site
def normalizeSite(site: str):
    locationLeft = -1
    locationRight = -1
    locationLeft = site.find("www.")
    locationRight = site.find(".com")
    return site[locationLeft+4:locationRight]

# Returns string of the command with spaces
def textToSearch(command):
    text: str = ""
    for x in command:
        if x != "search":
            text = text + " " + x
    return text
    
# FUNCTION to get all required Information to search a website
# RETURNS
#   Tuple
#       Boolean : True if site can be searched
#       Tuple : (str: Element type,str: Element Name)
#           
def requirment(site: str, command):
    siteName = normalizeSite(site)
    searchRequirment = isSearchable(siteName)
    text = textToSearch(command)
    if searchRequirment[0]: 
        elementInformation = elementTag.get(searchRequirment[1]) 
        return (True, text, elementInformation)
    else:
        return (False, "", ("",""))

print(textToSearch(["search", "1", "2", "3"]))