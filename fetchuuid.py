from github import Github
import json
import os
import subprocess
import uuid
from cookiecutter.main import cookiecutter

file_location = os.path.dirname(os.path.realpath(__file__))


g = Github("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")
user = g.get_user()
username = user.login
repo = g.get_repo('boylejack/kosmodulargrid')
fork = user.create_fork(repo)

script_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_path)     # ensure repo is cloned to directory containing script
command = "git clone https://github.com/" + username + "/kosmodulargrid.git"
subprocess.run(command) # clone forked repo to file_location


makers_file_location = script_path + "\kosmodulargrid\public\data\makers.json"
#makers_raw = open(makers_file_location,"r") # decode file

with open(makers_file_location) as f:
    makers_json = json.loads(f.read())
    f.close()

num_makers = len(makers_json) # count entries in loaded json
maker_dict = {}
for i in range(0,num_makers): # loop x times where x is number of entries
    makers = makers_json[i]  # load maker from that entry in list
    id = makers["id"] 
    name = makers["name"]
    print(id," ",name)
    maker_dict[name] = id # add name and id to dictionary



def checkname():
    uuid = ""
    queryname = input("Enter name of maker (EXACTLY as shown above, if it exists): ")
    if queryname in maker_dict: # check if it's in the list of known makers
        print("OK!")
        uuid = maker_dict[queryname]
        return queryname, uuid, False
    else: # if it's not in the list of known makers
        new = input("Maker " + queryname + "not found, would you like to create a new one? Enter Y/N").upper
        if new == "Y":
            uuid = str(uuid.uuid4())
            new_name = input("Enter new maker name again:")
            maker_dict[new_name] = uuid
            return new_name, uuid, True
        elif new == "N":
            print("Try again")
            checkname() # repeat until a known maker is entered

maker_name, maker_uuid, new_maker = checkname()

print("Name: " + maker_name + ", UUID: " + maker_uuid)

if new_maker == True:
    maker_desc = input("Enter new maker description (e.g LMNC forum user Sonosus):")
    maker_site = input("Enter new maker's website including https://:")
else:
    maker_desc = ""
    maker_site = ""

print("Generating template using cookiecutter. Input information at all prompts when requested then press return.")
print("WARNING: FOR PROMPTS maker_uuid ONWARDS, DO NOT ENTER ANY DATA. PRESS RETURN.")
print("THIS SCRIPT WILL GENERATE THESE VALUES FOR YOU.")
cookiecutter(file_location, extra_context={'maker_uuid':maker_uuid, 'maker_name':maker_name, 'maker_desc':maker_desc, 'maker_site':maker_site})

def rm_last_lines(file):
    original=open(file,"r")
    d=original.read()
    original.close()
    m=d.split("\n")
    s="\n".join(m[:-2])
    original=open(file,"w+")
    for i in range(len(s)):
        original.write(s[i])
    original.close()

rm_last_lines(file_location + "/kosmodulargrid/public/data/makers.json")
rm_last_lines(file_location + "/kosmodulargrid/public/data/modules.json")


def read_file(path):
    file = open(path, "r")
    snippet = file.read()
    file.close()
    return snippet

print(read_file(maker_name + '/maker.json'))



    

    
