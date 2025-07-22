@echo OFF
echo "================================="
echo "Setting up Python virtual environment..."
echo "================================="

REM Check if python is installed
python --version > NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo "Python is not installed or not in PATH. Please install Python 3."
    pause
    exit /b 1
)

REM Create virtual environment
if NOT EXIST venv (
    echo "Creating virtual environment 'venv'..."
    python -m venv venv
) else (
    echo "Virtual environment 'venv' already exists."
)

echo "================================="
echo "Activating virtual environment and installing dependencies..."
echo "================================="

call "venv\Scripts\activate.bat"
pip install -r requirements.txt

echo "================================="
echo "Setup complete. You can now run the bot using visa_bot_gui.py"
echo "Or by running the auto_run_bot.bat script."
echo "================================="
pause
