@echo off
:: setupdev.cmd - A simple script that installs disrichie's prerequisites
:: Check if Python 3 is installed
echo Check: Python 3
python --version > NUL
if errorlevel 1 goto pyCheckFailed

:: Also for pip
echo Check: PIP
pip --version > NUL
if errorlevel 1 goto pipCheckFailed

:: Install required modules
echo Install: Required Modules
pip install pypresence

:: Then exit the script
echo Done
goto:eof

:: Define some error functions
:pyCheckFailed
echo Error: Python 3 is required for disrichie to be ran, but is not installed.

:pipCheckFailed
echo Error: pip is required to install required modules for disrichie, and is not installed.