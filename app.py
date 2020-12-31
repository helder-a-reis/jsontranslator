import PySimpleGUI as sg
import json_flatten as jf
from fileUtils import *
from terms import *
        

# --------------------------------- Define Layout ---------------------------------
# inner layout with 2 columns
keyList = sg.Listbox(values=[], enable_events=True, size=(40,20), key='-KEYS-', select_mode="LISTBOX_SELECT_MODE_SINGLE")

left_col = [
    [sg.Text('Source file'), sg.In(size=(25,1), enable_events=True, key='-SOURCE-'), 
        sg.FileBrowse(button_text='Choose', file_types=(('JSON Files', '*.json'),))],
    [sg.Text('Target file'), sg.In(size=(25,1), enable_events=True, key='-TARGET-'), 
        sg.FileBrowse(button_text='Choose', file_types=(('JSON Files', '*.json'),))],
    [keyList]]

#startTranslationLayout = [[sg.Text('Choose a source file and key to see translations')]]
sourceText = sg.Multiline(key=('-SOURCETEXT-'), disabled=True)
targetText = sg.Multiline(key=('-TARGETTEXT-'))
right_col = [
    [sg.Text('Source'), sg.Text(key='-SOURCELOCALE-'), sourceText],
    [sg.Text('Target'), sg.Text(key='-TARGETLOCALE-'), targetText, sg.Button(button_text='Save', enable_events=True, key='-SAVE-')]
    ]

# ----- Full layout -----
layout = [[sg.Column(left_col), sg.VSeperator(), sg.Column(right_col)]]

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
        sourceFile = values['-SOURCE-']
        sourceDict = getDictFromJSON(sourceFile)
        sourceDictFlat = jf.flatten(sourceDict)
        keyList.update(values=list(sourceDictFlat.keys()))
        
        sourceLocale = getLocaleFromFileName(sourceFile)
        window['-SOURCELOCALE-'].update(value=getLocaleFromFileName(sourceFile))
        
    if event == '-TARGET-':
        targetFile = values['-TARGET-']
        targetDict = getDictFromJSON(targetFile)
        targetDictFlat = jf.flatten(targetDict)

    # key on the list clicked
    if event == '-KEYS-':
        # populate source
        sourceText.update(value=sourceDictFlat.get(keyList.get()[0]))
        if targetFile != '' :
            # populate target
            targetText.update(value=targetDictFlat.get(keyList.get()[0]))
            targetText.set_focus()

    if event == '-SAVE-':
        # update target dict
        targetDictFlat[keyList.get()[0]]=targetText.get().rstrip()
        # save target file
        targetDict = jf.unflatten(targetDictFlat)
        saveDictToJSON(targetDict, targetFile)

     

# --------------------------------- Close & Exit ---------------------------------

window.close()