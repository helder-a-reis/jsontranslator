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

def duplicateFile(sourceFileName, targetFileName):
    return copyfile(sourceFileName, targetFileName)

# returns a list of file names in the same folder as given file without extension
# user is responsible to ensure all files in folder are translation files
def getSiblingFileNames(sourceFile):
    theFolder = path.dirname(sourceFile)
    files = []
    for f in listdir(theFolder):
        if isfile:            
            files.append(path.splitext(path.basename(f))[0])

    return files

def getLocaleFromFileName(fileName):
    return path.splitext(path.basename(fileName))[0]