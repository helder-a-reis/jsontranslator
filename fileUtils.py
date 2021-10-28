import json
from shutil import copyfile
from os import path, listdir
from os.path import isfile, getsize

def getDictFromJSON(jsonFileName):
    jsonFile=open(jsonFileName, encoding='utf-8').read()
    # check empty file use an empty object to avoid parsing error
    if jsonFile == '':
        jsonFile = '{}'
    dict = json.loads(jsonFile)
    return dict

def saveDictToJSON(dict, jsonFileName):
    with open(jsonFileName, 'w', encoding='utf-8') as outfile:
        json.dump(dict, outfile, indent = 4, ensure_ascii=False, sort_keys=True)

def getLocaleFromFileName(fileName):
    return path.splitext(path.basename(fileName))[0]