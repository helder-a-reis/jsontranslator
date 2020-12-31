# JSON translator
Desktop application for translating JSON language files, for instance in a web project. Built with Python and PySimpleGUI.

## Create an exe
To create an exe use pyinstaller, run "pyinstaller jsontranslator.py -F"

## Usage
The program allows you to translate a json file (target file) based on another one (source file).

It was primarily designed to translate json files in an Angular project but should work with any 2 json file, as long as they have the same keys.

Run jsontranslator.py to launch from code or use the compiled jsontranslator.exe
1. Select a source file
2. Select a target locale
3. Enter a translation for the target
4. Click "Save" or "Save and Next"

## Notes
There's no undo, it's assumed you have your files under version control.
This is a side project, I update it when I have some spare time. If you use it please do report bugs and ideas for improvement! PRs welcome.

