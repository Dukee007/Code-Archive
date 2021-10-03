import json

def openf(file):
    return open(file)

def openedit(file):
    return open(file, "w+")

def savejson(file, jsonn):
    f = open(file, "w+")
    json.dump(jsonn, f)
    f.close()

def loadjson(file):
    f = open(file)
    return json.load(f)
