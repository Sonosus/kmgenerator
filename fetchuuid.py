import urllib.request 
import json

makers_url = 'https://raw.githubusercontent.com/boylejack/kosmodulargrid/main/public/data/makers.json'
with urllib.request.urlopen(makers_url) as file:
    makers_raw = file.read().decode('utf-8') # decode file
    
makers_json = json.loads(makers_raw)

num_makers = len(makers_json) # count entries in loaded json
maker_dict = {}
for i in range(0,num_makers): # loop x times where x is number of entries
    makers = json.loads(makers_raw)[i]  # load maker from that entry
    #print(type(makers)) #debug: print data type - should be dict
    id = makers['id'] 
    name = makers['name']
    print(id," ",name)
    maker_dict[name] = id # add name and id to dictionary

    #print(maker_dict) # debug: print dictionary of all makers

def checkname():
    queryname = input("Enter name of maker: ")
    if queryname in maker_dict: # check if it's in the list of known makers
        print("OK!")
        return queryname
    else: # if it's not in the list of known makers
        print("Maker name not found, please try again") 
        checkname() # repeat until a known maker is entered
print(checkname()) # debug: print checked name


    

    
