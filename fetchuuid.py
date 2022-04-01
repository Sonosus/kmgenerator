import urllib.request json #import required libs
with urllib.request.urlopen('https://raw.githubusercontent.com/boylejack/kosmodulargrid/main/public/data/makers.json') as f: # fetch remote json file
    makers_raw = f.read().decode('utf-8') # decode file
    maker_dict = {"name":"id"} # create empty placeholder dictionary

makers_count = len(json.loads(makers_raw)) # count entries in loaded json
for i in range(0,makers_count): # loop x times where x is number of entries
    makers = json.loads(makers_raw)[i]  # load maker from that entry
    #print(type(makers)) #debug: print data type - should be dict
    ids = makers['id'] # get maker uuid
    name = makers['name'] # get maker name
    print(ids," ",name) # print name and id
    maker_dict[name] = ids # add name and id to dictionary
print(maker_dict) # debug: print dictionary of all makers

def checkname(): #function checkname()
    queryname = input("Enter name of maker: ") # get name of maker to lookup
    if queryname in maker_dict: # check if it's in the list of known makers
        print("OK!")
        return queryname # return wanted maker
    else: # if it's not in the list of known makers
        print("Maker name not found, please try again") 
        checkname() # repeat until a known maker is entered
print(checkname()) # debug: print checked name


    

    
