@echo off
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.9+ and try again.
    pause
    exit /b
)

python -c "import tkinter, pydirectinput, ctypes, time" 2>nul
if %errorlevel% neq 0 (
    echo Installing required libraries...
    python -m pip install --upgrade pip
    pip install tkinter pydirectinput ctypes time
)

start /min pythonw "SapMacro.py"
exit