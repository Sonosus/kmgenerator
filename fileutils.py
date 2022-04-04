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

def read_file(path):
    file = open(path, "r")
    data = file.read()
    file.close()
    return data

def append_to_file(path, data):
    file = open(path, "a")
    file.write(data)
    file.close()