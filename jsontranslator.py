from os import path

from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from fileUtils import *
from terms import *

#initial frame setup
root = Tk()
root.title("Translate JSON files")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
    
#app variables    
targetLocales = ()

sourceFileName = StringVar()
sourceFileName.set("None")
sourceLocale = StringVar()
sourceLocale.set("None")
sourceDict = {}

targetFileName = StringVar()
targetLocale = StringVar()
targetDict = {}

entry = {}

#list of terms with key, source and target
terms = []

#workflow: 1) open source file 2) create term list with key and source 3) open target file (create if new) 4) populate term list target 5) show all 6) save targets

def openSourceFile():
    global terms
    global sourceDict
    #returns the file name, NOT the file
    fileToOpen = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
    sourceFileName.set(fileToOpen)
    sourceLocale.set(path.splitext(path.basename(fileToOpen))[0])

    #populate target options
    targetLocales = getSiblingFileNames(sourceFileName.get())
    targetLocales.remove(sourceLocale.get())
    targetDrop.set_menu(*targetLocales)

    #load json content as dict
    sourceDict = getDictFromJSON(fileToOpen)
    #populate list of terms with key and source
    terms = initializeTerms(sourceDict)
       

def openTargetFile():
    global targetDict
    targetFileName.set(sourceFileName.get().replace(sourceLocale.get(), targetLocale.get()))
    targetDict = getDictFromJSON(targetFileName.get())
    
    addTargetToTerms(terms, targetDict)
    populateContent(terms)


def populateContent(terms):
    ttk.Label(contentFrame, text="Key", font='bold').grid(column=1, row=0, sticky=W)
    ttk.Label(contentFrame, text="Source", font='bold').grid(column=2, row=0, sticky=W)
    ttk.Label(contentFrame, text="Target", font='bold').grid(column=3, row=0, sticky=W)

    i=1
    for term in terms:
        ttk.Label(contentFrame, text=term.key).grid(column=1, row=i, sticky=W)
        ttk.Label(contentFrame, text=term.source).grid(column=2, row=i, sticky=W)
        e = ttk.Entry(contentFrame)
        e.grid(column=3, row=i, sticky=W)
        entry[term.key] = e
        e.insert(0, term.target)

        i=i+1


def saveTarget():
    global sourceDict
    global terms   
    # make a copy of the source dict just with keys
    newTargetDict = cleanDict(terms, sourceDict)
    for term in terms:
        translateInDict(newTargetDict, term.key, entry[term.key].get())

    # remove empty values
    newTargetDict = removeEmpties(newTargetDict)
    saveDictToJSON(newTargetDict, targetFileName.get())

def quit():
    root.destroy()

#control section
controlFrame = ttk.LabelFrame(mainframe, text="Files and Languages")
controlFrame.grid(column=0, row=0, sticky=(N, W, E, S))

#source
ttk.Label(controlFrame, text="1. Select source file").grid(column=1, row=1, sticky=W)
ttk.Button(controlFrame, text="Choose...", command=openSourceFile).grid(column=2, row=1, sticky=E)
ttk.Label(controlFrame, textvariable=sourceFileName).grid(column=3, row=1, sticky=W)

#target
ttk.Label(controlFrame, text="2. Select target language").grid(column=1, row=2, sticky=W)
targetDrop = ttk.OptionMenu(controlFrame, targetLocale, *targetLocales)
targetDrop.grid(column=2, row=2, sticky=E)
ttk.Button(controlFrame, text="Go!", command=openTargetFile).grid(column=3, row=2, sticky=W)


#content section
contentFrame = ttk.LabelFrame(mainframe, text="Content")
contentFrame.grid(column=0, row=1, sticky=(N, W, E, S))


#action section
actionFrame = ttk.Frame(mainframe)
actionFrame.grid(column=0, row=2)
ttk.Button(actionFrame, text="Save", command=saveTarget).grid(column=0, row=1, sticky=W)
ttk.Button(actionFrame, text="Quit", command=quit).grid(column=1, row=1, sticky=W)

#show
root.mainloop()
