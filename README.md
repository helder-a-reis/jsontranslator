# jsontranslator
Desktop application for finding and translating JSON language files in a web project. Built with Python and TkInter.

Takes one json file and translates it into other languages.
The system finds all files in the same folder as the source file - use is responsible to ensure all are translation files.
Run app.py to launch.
1. Select a source file
2. Select a target locale
3. Save your changes

## Create an exe
To create an exe use pyinstaller, run "pyinstaller jsontranslator.py -F"