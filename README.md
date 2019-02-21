# jsontranslator
Desktop application for finding and translating JSON language files in a web project. Built with Python and TkInter.

Currently takes one json file and translates it into other languages.
The system expects files in "locale.json" format (en_us.json, es_es.json) - might make this configurable in the future.
Run app.py to launch.
1. Select a source file
2. Select a target locale (configure others in the supportedLocales variable)
3. If a file with that locale doesn't exist, app will create one
4. Save your changes
