from contextlib import suppress

class Translation:
    def __init__(self, locale):
        self.locale = locale
        self.terms = {}

    def __init__(self, locale, terms):
        self.locale = locale
        self.terms = terms


class Term:
    #initialize a term with key and source
    def __init__(self, key, source):
        self.key = key
        self.source = source
        self.target = ""

    def __str__(self):
        return self.key

#initialize a list of terms with a source dictionary
def initializeTerms(sourceDict):
    terms = []

    def addTerm(sourceDict):
        for key, value in sourceDict.items():
            #if the value itself is a dictionary do a recursive call
            if isinstance(value, dict):
                addTerm(value)
            else:
                term = Term(key, value)
                terms.append(term)

    addTerm(sourceDict)

    return terms

def extractKeys(sourceDict):
    keys = []
    def addKey(sourceDict):
        for key, value in sourceDict.items():
            if isinstance(value, dict):
                addKey(value)
            else:
                keys.append(key)
    
    addKey(sourceDict)
    
    return keys

#adds targets from a dictionary to a list of terms
def addTargetToTerms(terms, targetDict):
    def addTarget(targetDict):
        for key, value in targetDict.items():
            if isinstance(value, dict):
                addTarget(value)
            else:
                for term in terms:
                    if term.key == key:
                        newTerm = Term(key, term.source)
                        newTerm.target = value
                        terms.remove(term)
                        terms.append(newTerm)

    addTarget(targetDict)

    return terms

#updates target dictionary from a list of terms
def updateDict(terms, targetDict):
    for term in terms:
        targetDict = translateInDict(targetDict, term.key, term.target)
    return targetDict

#returns dictionary with empty values
def cleanDict(terms, targetDict):
    for term in terms:
        targetDict = translateInDict(targetDict, term.key, '')
    return targetDict

#removes elements with empty values
def removeEmpties(aDict):
    # keys to delete
    keys = []

    def findEmptyValues(dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                findEmptyValues(value)
            else:
                if value == '':
                    keys.append(key)


    def delete_keys_from_dict(dictionary, keys):
        for key in keys:
            with suppress(KeyError):
                del dictionary[key]
        for value in dictionary.values():
            if isinstance(value, dict):
                delete_keys_from_dict(value, keys)

    findEmptyValues(aDict)
    
    delete_keys_from_dict(aDict, keys)

    return aDict   


#updates a value in a dictinary
def translateInDict(targetDict, updateKey, updateValue):
    for key, value in targetDict.items():
        #if the value itself is a dictionary do a recursive call
        if isinstance(value, dict):
            translateInDict(value, updateKey, updateValue)
        else:
            if key == updateKey:
                targetDict[key] = updateValue
                break
    return targetDict

# returns a translation for a key in a dictionary or None if not present
def getTermInDict(theDict, searchKey):
    found = None

    def findTerm(theDict, searchKey):
        for key, value in theDict.items():
            if isinstance(value, dict):
                findTerm(value, searchKey)
            else:
                if key == searchKey:
                    return value
    
    return findTerm(theDict, searchKey)