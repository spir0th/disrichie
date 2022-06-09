@echo off
:: pack-portable - A script that packages disrichie into a portable binary executable using pyinstaller
:: ONLY EXECUTE THIS WHEN YOU'RE IN THE DISRICHIE SOURCE DIRECTORY
:: Make sure pyinstaller is already installed otherwise it'll fail to package
echo Check: pyinstaller Modules
pyinstaller --version > NUL
if errorlevel 1 goto pyinstallerCheckFailed

:: Then start the packaging process
echo Start: Process Package Portable
call :startPackage

:: Exit the script after
echo Done
goto:eof

:: Define some functions
:startPackage
echo Package: Build
pyinstaller --onefile --clean --noconfirm --path scripts --specpath dist --workpath dist/build disrichie
goto:eof

:pyinstallerCheckFailed
echo Error: pyinstaller is required for packaging disrichie into a binary executable, and is not installed.
echo Install it using: pip install pyinstaller
goto:eof