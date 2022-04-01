import urllib.request
import json
with urllib.request.urlopen('https://raw.githubusercontent.com/boylejack/kosmodulargrid/main/public/data/makers.json') as f:
    #data = json.loads(url.read().decode())
    makers_raw = f.read().decode('utf-8')
    maker_dict = {"name":"id"}
print(type(makers_raw))
makers_count = len(json.loads(makers_raw))
for i in range(0,makers_count):
    makers = json.loads(makers_raw)[i]
    #print(type(makers))
    ids = makers['id']
    name = makers['name']
    print(ids," ",name)
    maker_dict[name] = ids
print(maker_dict)

def checkname():
    queryname = input("Enter name of maker: ")
    if queryname in maker_dict:
        print("OK!")
        return queryname
    else:
        print("Maker name not found, please try again")
        checkname()
print(checkname())


    

    
