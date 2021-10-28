import PySimpleGUI as sg
import json_flatten as jf
import webbrowser
from fileUtils import *
from terms import *

# --- variables ---
sourceDictFlat = {}
targetDictFlat = {}
unsavedChanges = False
lastSelectedKey = None

# ---- UI helper functions -----

# updates source text with currently selected key
def updateSource():
    sourceText.update(value=sourceDictFlat.get(keyList.get()[0], ''))

def updateTarget():
    text = targetDictFlat.get(keyList.get()[0], '')
    targetText.update(value=targetDictFlat.get(keyList.get()[0], ''))
    unsavedChange = False

def clearTranslations():
    sourceText.update('')
    targetText.update('')

def saveTarget():
    # update target dict
    targetDictFlat[lastSelectedKey]=targetText.get().rstrip()
    # save target file
    targetDict = jf.unflatten(targetDictFlat)
    saveDictToJSON(removeEmpties(targetDict), targetFile.get())
    
# --------------------------------- Define Layout ---------------------------------

sourceFile = sg.In(size=(60,1), enable_events=True, key='-SOURCE-', readonly=True)
targetFile = sg.In(size=(60,1), enable_events=True, key='-TARGET-', readonly=True)
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
targetText = sg.Multiline(key=('-TARGETTEXT-'), size=(50, 8), enable_events=True)
saveButton = sg.Button(button_text='Save', enable_events=True, key='-SAVE-')
saveAndNextButton = sg.Button(button_text='Save and Next', enable_events=True, key='-SAVEANDNEXT-')
autoSaveCheck = sg.Checkbox('Auto save changes as you type', enable_events=True, key='-AUTOSAVE-')
exportButton = sg.Button(button_text="Export all to file", enable_events=True, key='-EXPORT-')
exportMissingButton = sg.Button(button_text="Export missing translations", enable_events=True, key='-EXPORTMISSING-')
right_col = [
    [sourceLocale, sourceText],
    [targetLocale, targetText],
    [saveButton, saveAndNextButton],
    [autoSaveCheck],
    [exportButton, exportMissingButton]
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

    if event == '-TARGETTEXT-':
        # auto save every time user types
        if autoSaveCheck.get() == 1:
            saveTarget()
            unsavedChanges = False
        else:
            unsavedChanges = True

    # key on the list clicked
    if event == '-KEYS-':       
        if unsavedChanges:
            saveChanges = sg.PopupYesNo('Save changes?', title='Unsaved changes')
            if saveChanges == 'Yes':
                saveTarget()
            unsavedChanges = False

        # populate source
        updateSource()
        if targetFile.get() != '' :
            # populate target
            updateTarget()
            targetText.set_focus()
        lastSelectedKey = keyList.get()[0]
    
    if event == '-MISSING-':
        if missingCheck.get() == 1:
            keyList.update(values=getKeysMissingTarget(sourceDictFlat, targetDictFlat))
        else:
            keyList.update(values=list(sourceDictFlat.keys()))
        clearTranslations()

    if event == '-SAVE-':
        saveTarget()
        unsavedChanges = False

    if event == '-SAVEANDNEXT-':
        saveTarget()
        currentIndex = keyList.GetIndexes()[0]
        if currentIndex+1 < len(keyList.GetListValues()):
            keyList.update(set_to_index=currentIndex+1)
            updateSource()
            updateTarget()
        unsavedChanges = False

    if event == '-AUTOSAVE-':
        if autoSaveCheck.get() == 1:
            if (sg.PopupOKCancel('This will save the json file as you type, changes can not be undone - proceed?')) == 'OK':
                # disable save buttons
                saveButton.Update(disabled=True)
                saveAndNextButton.Update(disabled=True)
            else:
                autoSaveCheck.Update(value=False)
        else:
            saveButton.Update(disabled=False)
            saveAndNextButton.Update(disabled=False)

    if event == '-EXPORT-':
        exportToFile(sourceDictFlat, targetDictFlat, sourceLocale.get(), targetLocale.get())

    if event == '-EXPORTMISSING-':
        exportToFile(sourceDictFlat, targetDictFlat, sourceLocale.get(), targetLocale.get(), True)

    if event == 'Usage':
        sg.PopupOK('Choose a source file, then a target file, click on a key, translate target, save. If a locale does not exist yet simply create a new empty json file.', 
        title='How to use this program', grab_anywhere=True)

    if event == 'About':
        sg.PopupOK('Developed by Helder Reis', title='About')

    if event == 'Github':
        webbrowser.open_new_tab('https://github.com/helder-a-reis/jsontranslator')

# --------------------------------- Close & Exit ---------------------------------

window.close()