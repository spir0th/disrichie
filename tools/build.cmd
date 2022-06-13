@echo off
:: build - A script that converts disrichie into a binary executable using pyinstaller
:: ONLY EXECUTE THIS WHEN YOU'RE IN THE DISRICHIE SOURCE DIRECTORY
:: Make sure pyinstaller is already installed otherwise it'll fail to package
echo Check: pyinstaller Modules
pyinstaller --version > NUL
if errorlevel 1 goto pyinstallerCheckFailed

:: Then start the packaging process=
call :startPackage

:: Exit the script after
echo Done
goto:eof

:: Define some functions
:startPackage
echo Start: Build Standalone version
pyinstaller disrichie --clean --noconfirm ^
	--icon "../assets/disrichie.ico" --path "./scripts" ^
	--workpath "./dist/build" --specpath "./dist" ^
	--version-file "../assets/version_info.txt"
goto:eof

:pyinstallerCheckFailed
echo Error: pyinstaller is required for packaging disrichie into a binary executable, and is not installed.
echo Install it using: pip install pyinstaller
goto:eof