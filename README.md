# jsontranslator
Desktop application for finding and translating JSON language files in a web project. Built with Python and TkInter.

## Create an exe
To create an exe use pyinstaller, run "pyinstaller jsontranslator.py -F"

## Usage
The program allows you to translate a json file by seeing its source and target files side by side.

It was primarily designed to translate json files in an Angular project, so it expects a structure of one json files per language all located in the same folder (for example a i18n folder with en.json, pt-PT.json, de-DE.json, etc).

The system finds all files in the same folder as the source file - user is responsible to ensure all are json translation files.

Run jsontranslator.py to launch from code or use the compiled jsontranslator.exe
1. Select a source file
2. Select a target locale
3. Save your changes

