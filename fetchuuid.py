import github
import json
import os
import subprocess
import uuid as uuidgen
from cookiecutter.main import cookiecutter
import fileutils
import shutil
from datetime import datetime
from git import Repo

#fetch base directory path
script_path = os.path.dirname(os.path.realpath(__file__))

# initialize github and fork repo
print("Connecting to GitHub and forking repo...")

raw_key = fileutils.read_file("key.txt")
key = raw_key.strip("\n")

g = github.Github(key)
user = g.get_user()
username = user.login
repo = g.get_repo('boylejack/kosmodulargrid')
fork = user.create_fork(repo)
upstream_user = g.get_user('boylejack')
print("Done!")

# set up pygithub
repo = Repo.clone_from(https://)


# clone repo to local directory
print("Cloning repository to local folder...")
script_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_path)     # ensure repo is cloned to directory containing script
command = "git clone https://github.com/" + username + "/kosmodulargrid"
os.system(command) # clone forked repo to script_path
print("Done!")

# define path to data we want to modify
makers_file = script_path + "/kosmodulargrid/public/data/makers.json"
modules_file = script_path + "/kosmodulargrid/public/data/modules.json"
#makers_raw = open(makers_file,"r") # decode file

print("Loading and parsing makers.json...")
# load makers.json
with open(makers_file) as f:
    makers_json = json.loads(f.read())
    f.close()
print("Makers parsed:")
#parse makers.json into dictionary
num_makers = len(makers_json) # count entries in loaded json
maker_dict = {}
for i in range(0,num_makers): # loop through list n times
    makers = makers_json[i]  # load maker from that entry in list
    id = makers["id"] 
    name = makers["name"]
    print("UUID:  " + id + "    Name:  " + name)
    maker_dict[name] = id # add name and id to dictionary
print("Done!")


def checkname():
    uuid = ""
    queryname = input("Enter name of maker (EXACTLY as shown above, if it exists): ")
    if queryname in maker_dict: # check if it's in the list of known makers
        print("OK!")
        uuid = maker_dict[queryname]
        return queryname, uuid, False
    else: # if it's not in the list of known makers
        print("Maker " + queryname + " not found, creating new maker.")
        uuid = str(uuidgen.uuid4())
        new_name = input("Enter new maker name again:")
        maker_dict[new_name] = uuid
        if new_name != queryname:
            raise NameError
        return new_name, uuid, True

#get maker details from input function
maker_name, maker_uuid, new_maker = checkname()

#print out all maker names and ids
print("Name: " + maker_name + ", UUID: " + maker_uuid)

#gather data for new maker
if new_maker == True:
    maker_desc = input("Enter new maker description (e.g LMNC forum user Sonosus):")
    maker_site = input("Enter new maker's website including https://:")
else:
    maker_desc = ""
    maker_site = ""

def ask_new():
    answer = input("Create another module? Y/N: ")
    if answer == "Y":
        return  True
    elif answer == "N":
        return False
    else:
        print("Input not recognised, try again.")
        ask_new()

keep_going = True
while keep_going:
    print("Generating template using cookiecutter. Input information at all prompts when requested then press return.")
    print("WARNING: FOR PROMPTS maker_uuid ONWARDS, DO NOT ENTER ANY DATA. PRESS RETURN.")
    print("THIS SCRIPT WILL GENERATE THESE VALUES FOR YOU.")
    
    #generate files with cookiecutter
    cookiecutter(script_path, extra_context={'maker_uuid':maker_uuid, 'maker_name':maker_name, 'maker_desc':maker_desc, 'maker_site':maker_site})
    
    #copy modules to git repo
    print("Adding module to modules.json...")
    fileutils.rm_last_lines(script_path + "/kosmodulargrid/public/data/modules.json")
    module_snippet = ",\n" + fileutils.read_file(maker_name + '/module.json')
    fileutils.append_to_file(modules_file, module_snippet)
    print("Done!")
    
    #delete buffer file
    print("Deleting temporary modules file...")
    os.remove(script_path + "/" + maker_name + "/module.json")
    print("Done!")

    # do we want more modules?
    keep_going = ask_new()

# if maker does not exist, add their details in the repo
if new_maker:
    print("Adding new maker to makers.json...")
    fileutils.rm_last_lines(script_path + "/kosmodulargrid/public/data/makers.json")
    maker_snippet = ",\n" + fileutils.read_file(maker_name + '/maker.json')
    fileutils.append_to_file(makers_file, maker_snippet)
    print("Done!")

#delete cookiecutter's generated directory
print("Deleting temporary data folder...")
shutil.rmtree(script_path + "/" + maker_name)
print("Done!")

# add all files to git and commit them
print("Adding files and committing to Git repository...")
cloned_dir = script_path + "/kosmodulargrid"
os.chdir(cloned_dir) # make sure we're acting on the cloned repo, not script's repo
os.system("git add -A",)
os.system('git commit -m "Add modules generated by kmgenerator, a program maintained by Sonosus (github.com/sonosus/kmgenerator)')
print("Done!")

# git push files to remote fork
print("Pushing local repository to GitHub...")
os.system("git push")
print("Done!")


print("Starting pull request on GitHub...")
time = datetime.now()
timestamp = time.strftime("%d-%b-%Y at %H:%M:%S")
pr_title = "Add " + maker_name + " modules"
pr_message = "Add modules by " + maker_name + ".\nPull request generated by [kmgenerator](https://github.com/sonosus/kmgenerator) on " + timestamp
pr = repo.create_pull(pr_title, pr_message, "main", '{}:{}'.format(username, 'main'), False)
print("Done! view your pull request at https://github.com/boylejack/kosmodulargrid/pulls")

#clean up files
print("Deleting cloned repository...")
shutil.rmtree(script_path + "/kosmodulargrid")
print("Done!")