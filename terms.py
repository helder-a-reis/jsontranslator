
class Term:
    def __init__(self, key, word):
        self.key = key
        self.word = word


def getListTermsFromDict(dictToParse):
    terms = []

    def addTerm(dictToParse):
        for key, value in dictToParse.items():
            #if the value itself is a dictionary do a recursive call
            if isinstance(value, dict):
                addTerm(value)
            else:
                term = Term(key, value)
                terms.append(term)

    addTerm(dictToParse)

    return terms


#updates the key(s) in dict with newValue
def translateInDict(dict, key, newValue):
    for key, value in dict.items():
        #if the value itself is a dictionary do a recursive call
        if isinstance(value, dict):
            translateInDict(value, key, newValue)
        else:
            dict[key] = newValue
    
    return dict