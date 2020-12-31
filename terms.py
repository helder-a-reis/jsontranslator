from contextlib import suppress

class Term:
    #initialize a term with key and source
    def __init__(self, key, source):
        self.key = key
        self.source = source
        self.target = ""

    def __str__(self):
        return self.key


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
