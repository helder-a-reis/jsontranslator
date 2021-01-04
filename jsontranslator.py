import PySimpleGUI as sg
import json_flatten as jf
import webbrowser
from fileUtils import *
from terms import *

# --- variables ---
sourceDictFlat = {}
targetDictFlat = {}

# ---- UI helper functions -----

# updates source text with currently selected key
def updateSource():
    sourceText.update(value=sourceDictFlat.get(keyList.get()[0], ''))

def updateTarget():
    text = targetDictFlat.get(keyList.get()[0], '')
    targetText.update(value=targetDictFlat.get(keyList.get()[0], ''))

def saveTarget():
    # update target dict
    targetDictFlat[keyList.get()[0]]=targetText.get().rstrip()
    # save target file
    targetDict = jf.unflatten(targetDictFlat)
    saveDictToJSON(removeEmpties(targetDict), targetFile.get())
    

# --------------------------------- Define Layout ---------------------------------

sourceFile = sg.In(size=(60,1), enable_events=True, key='-SOURCE-')
targetFile = sg.In(size=(60,1), enable_events=True, key='-TARGET-')
header = [
    [sg.Text('Source file', size=(10, 1)), sourceFile, sg.FileBrowse(button_text='Choose', file_types=(('JSON Files', '*.json'),))],
    [sg.Text('Target file', size=(10, 1)), targetFile, sg.FileBrowse(button_text='Choose', file_types=(('JSON Files', '*.json'),))],
    ]

keyList = sg.Listbox(values=[], enable_events=True, size=(50,30), key='-KEYS-', select_mode="LISTBOX_SELECT_MODE_SINGLE")
missingCheck = sg.Checkbox('Show only missing translations', enable_events=True, key='-MISSING-')
left_col = [[missingCheck],
    [keyList]]

sourceLocale = sg.Text(text='Source', key='-SOURCELOCALE-', size=(6, 1))
targetLocale = sg.Text(text='Target', key='-TARGETLOCALE-', size=(6, 1))
sourceText = sg.Multiline(key=('-SOURCETEXT-'), disabled=True, size=(50, 8))
targetText = sg.Multiline(key=('-TARGETTEXT-'), size=(50, 8))
right_col = [
    [sourceLocale, sourceText],
    [targetLocale, targetText],
    [sg.Button(button_text='Save', enable_events=True, key='-SAVE-'), sg.Button(button_text='Save and Next', enable_events=True, key='-SAVEANDNEXT-')]
    ]

menu_def = [['Help', ['Usage', 'About', 'Github']]]
# ----- Full layout -----
layout = [
    [sg.Menu(menu_def)],
    [sg.Column(header)],
    [sg.Column(left_col), sg.VSeperator(), sg.Column(right_col, vertical_alignment='top', element_justification='center')]
    ]

# --------------------------------- Create Window ---------------------------------
window = sg.Window('JSON Translator', layout)

# ----- Run the Event Loop -----
# --------------------------------- Event Loop ---------------------------------
while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    # new source file selected
    if event == '-SOURCE-':  
        # clear the keys list
        keyList.update(values=[])               
        sourceDict = jf.flatten(getDictFromJSON(sourceFile.get()))
        sourceDictFlat = (sourceDict)
        keyList.update(values=list(sourceDictFlat.keys()))
        sourceLocale.update(value=getLocaleFromFileName(sourceFile.get()), visible=True)
        
    if event == '-TARGET-':
        targetDict = getDictFromJSON(targetFile.get())
        targetDictFlat = jf.flatten(targetDict)
        targetLocale.update(value=getLocaleFromFileName(targetFile.get()), visible=True)

    # key on the list clicked
    if event == '-KEYS-':
        # populate source
        updateSource()
        if targetFile.get() != '' :
            # populate target
            updateTarget()
            targetText.set_focus()
    
    if event == '-MISSING-':
        if missingCheck.get() == 1:
            keyList.update(values=getKeysMissingTarget(sourceDictFlat, targetDictFlat))
        else:
            keyList.update(values=list(sourceDictFlat.keys()))

    if event == '-SAVE-':
        saveTarget()

    if event == '-SAVEANDNEXT-':
        saveTarget()
        currentIndex = keyList.GetIndexes()[0]
        if currentIndex+1 < len(keyList.GetListValues()):
            keyList.update(set_to_index=currentIndex+1)
            updateSource()
            updateTarget()

    if event == 'Usage':
        sg.PopupOK('Choose a source file, then a target file, click on a key, translate target, save. If a locale does not exist yet simply create a new empty json file.', 
        title='How to use this program', grab_anywhere=True)

    if event == 'About':
        sg.PopupOK('Developed by Helder Reis', title='About')

    if event == 'Github':
        webbrowser.open_new_tab('https://github.com/helder-a-reis/jsontranslator')

# --------------------------------- Close & Exit ---------------------------------

window.close()