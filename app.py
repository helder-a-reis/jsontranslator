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
supportedLocales = {'en_US', 'es_ES', 'fr_FR', 'it_IT'}

sourceFileName = StringVar()
sourceFileName.set("None")
sourceLocale = StringVar()
sourceLocale.set("None")
sourceDict = {}

targetFileName = StringVar()
targetLocale = StringVar()
targetDict = {}

def openSourceFile():
    #returns the file name, NOT the file
    fileToOpen = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
    sourceFileName.set(fileToOpen)
    sourceLocale.set(path.splitext(path.basename(fileToOpen))[0])
    sourceDict = getDictFromJSON(fileToOpen)

    #populate source terms
    sourceTerms = getListTermsFromDict(sourceDict)
    i=1
    for term in sourceTerms:
        ttk.Label(keyFrame, text=term.key).grid(column=1, row=i, sticky=W)
        ttk.Label(sourceFrame, text=term.word).grid(column=1, row=i, sticky=W)
        i=i+1

    #remove source locale from options
    supportedLocales.remove(sourceLocale.get())
    TargetDrop


def openTargetFile():
    targetFileName.set(sourceFileName.get().replace(sourceLocale.get(), targetLocale.get()))
    #if file doesn't exist then create it first
    try:
            targetDict = getDictFromJSON(targetFileName.get())
    except:
            duplicateFile(sourceFileName.get(), targetLocale.get())
            targetDict = getDictFromJSON(targetFileName.get())
    
    #populate source terms
    targetTerms = getListTermsFromDict(targetDict)
    entry = {}
    i=1
    for term in targetTerms:
        #ttk.Entry(targetFrame, textvariable=term.word).grid(column=1, row=i, sticky=W)
        e = ttk.Entry(targetFrame)
        e.grid(column=1, row=i, sticky=W)
        entry[term] = e
        e.insert(0, term.word)

        i=i+1

def saveTarget():
    print("Saving")
    saveDictToJSON(targetDict, targetFileName.get())

def quit():
    root.destroy()

#control section
controlFrame = ttk.Frame(mainframe)
controlFrame.grid(column=0, row=0, sticky=(N, W, E, S))

#source
ttk.Label(controlFrame, text="1. Select source file").grid(column=1, row=1, sticky=W)
ttk.Button(controlFrame, text="Choose...", command=openSourceFile).grid(column=2, row=1, sticky=E)
ttk.Label(controlFrame, textvariable=sourceFileName).grid(column=3, row=1, sticky=W)

#target
ttk.Label(controlFrame, text="2. Select target language").grid(column=1, row=2, sticky=W)
TargetDrop = ttk.OptionMenu(controlFrame, targetLocale, *supportedLocales)
TargetDrop.grid(column=2, row=2, sticky=E)
ttk.Button(controlFrame, text="Go!", command=openTargetFile).grid(column=3, row=2, sticky=W)


#content section
contentFrame = ttk.Frame(mainframe)
contentFrame.grid(column=0, row=1, sticky=(N, W, E, S))

contentPane = ttk.Panedwindow(contentFrame, orient=HORIZONTAL)

keyFrame = ttk.LabelFrame(contentPane, text="key", width=200, height=100)
contentPane.add(keyFrame)
sourceFrame = ttk.LabelFrame(contentPane, text="source", width=300, height=100)
contentPane.add(sourceFrame)
targetFrame = ttk.LabelFrame(contentPane, text="target", width=300, height=100)
contentPane.add(targetFrame)
contentPane.grid(column=1, row=4)

#action section
actionFrame = ttk.Frame(mainframe)
actionFrame.grid(column=0, row=2)
ttk.Button(actionFrame, text="Save", command=saveTarget).grid(column=0, row=1, sticky=W)
ttk.Button(actionFrame, text="Quit", command=quit).grid(column=1, row=1, sticky=W)

#show
root.mainloop()
