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

def openSourceFile():
    #returns the file name, NOT the file
    fileToOpen = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
    fullFileName.set(fileToOpen)
    sourceLocale.set(path.splitext(path.basename(fileToOpen))[0])
    sourceDict = getDictFromJSON(fileToOpen)

    #print source terms
    sourceTerms = getListTermsFromDict(sourceDict)
    i=1
    for term in sourceTerms:
        #ttk.Label(sourceFrame, text=key).grid(column=1, row=1)
        print("new term: " + term.key + " " + term.word)
        ttk.Label(keyFrame, text=term.key).grid(column=1, row=i, sticky=W)
        ttk.Label(sourceFrame, text=term.word).grid(column=1, row=i, sticky=W)
        i=i+1

    
    
#variables    
fullFileName = StringVar()
sourceLocale = StringVar()
sourceDict = {}

#control section
controlFrame = ttk.Frame(mainframe)
controlFrame.grid(column=0, row=0, sticky=(N, W, E, S))
ttk.Button(controlFrame, text="Open JSON file", command=openSourceFile).grid(column=1, row=1, sticky=W)
    #show file info
ttk.Label(controlFrame, text="File:").grid(column=1, row=1, sticky=(E))
ttk.Label(controlFrame, textvariable=fullFileName).grid(column=2, row=2, sticky=(W))
ttk.Label(controlFrame, text="Source locale:").grid(column=1, row=3, sticky=(E))
ttk.Label(controlFrame, textvariable=sourceLocale).grid(column=2, row=3, sticky=(W))

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




#show
root.mainloop()
