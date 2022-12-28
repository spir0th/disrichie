@echo off
python --version > NUL
if errorlevel 1 goto pyCheckFailed

pip --version > NUL
if errorlevel 1 goto pipCheckFailed

pip install pypresence pyinstaller
goto:eof

:pyCheckFailed
echo Error: Python 3 is not installed.
goto:eof

:pipCheckFailed
echo Error: pip is not installed. Refer to Python Manuals for installation.
goto:eof