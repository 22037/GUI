# GUI
How to get Qt Designer
1. Download Qt Designer
https://build-system.fman.io/qt-designer-download
2. Helpful tutorial which also shows the method of how to translate ui code into
python code.
https://www.youtube.com/watch?v=FVpho_UiDAY

Convert ui code to Python code
1. Create a blank python file and have it in the same place as the ui file.
2. Open command prompt and change directory to where the ui file is.
3. Type in the following:
pyuic5 -x Name_of_the_ui_file.ui -o Name_of_the_python_file.py
4. Enter
5. When you open the python file, it will have your ui translated into python code.

Note
1. When running the python file, you will need the test_display.py to be in the current
directly that VisualStudio of whatever code system is reading.
