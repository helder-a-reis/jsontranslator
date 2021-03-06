import json
from shutil import copyfile
from os import path, listdir
from os.path import isfile

def getDictFromJSON(jsonFileName):
    jsonFile=open(jsonFileName, encoding='utf-8').read()
    dict = json.loads(jsonFile)
    return dict

def saveDictToJSON(dict, jsonFileName):
    with open(jsonFileName, 'w', encoding='utf-8') as outfile:
        json.dump(dict, outfile, indent = 4, ensure_ascii=False)

def getLocaleFromFileName(fileName):
    return path.splitext(path.basename(fileName))[0]