@echo OFF
REM This script launches the Visa Bot Graphical User Interface (GUI).
REM It assumes you have already run setup.bat to create the virtual environment.

echo "================================="
echo "Launching Visa Bot GUI..."
echo "================================="

REM Activate virtual environment
call "venv\Scripts\activate.bat"

REM Run the GUI script
python visa_bot_gui.py

echo "================================="
echo "GUI closed."
echo "================================="
pause 