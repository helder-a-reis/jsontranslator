import json

def getDictFromJSON(jsonFileName):
    jsonFile=open(jsonFileName).read()
    dict = json.loads(jsonFile)
    return dict
