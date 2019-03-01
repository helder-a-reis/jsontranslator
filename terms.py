
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