@echo off
REM Build script for Windows using PyInstaller
REM Creates a single-file executable that includes the data directory

REM Ensure running from project root
cd /d "%~dp0"

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate

REM Upgrade pip and install pyinstaller
python -m pip install --upgrade pip
pip install pyinstaller

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist todo_list_tracker.spec del /f /q todo_list_tracker.spec

REM Build single-file executable, include the data folder
pyinstaller --noconfirm --onefile --add-data "data;data" --name todo_list_tracker todo_list_tracker.py

REM Deactivate virtualenv
deactivate

echo Build finished. See dist\todo_list_tracker.exe