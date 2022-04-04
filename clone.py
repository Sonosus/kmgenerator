from github import Github
import os
import subprocess


file_location = os.path.dirname(os.path.realpath(__file__))

g = Github("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")
user = g.get_user()
repo = g.get_repo('boylejack/kosmodulargrid')
fork = user.create_fork(repo)

os.chdir(file_location)

subprocess.run("git clone https://github.com/boylejack/kosmodulargrid.git")
file_location = os.path.dirname(os.path.realpath(__file__))
print(file_location)