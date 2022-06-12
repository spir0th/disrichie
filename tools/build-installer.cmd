@echo off
:: build-installer - A script that converts the disrichie installer into a binary executable using pyinstaller
:: ONLY EXECUTE THIS WHEN YOU'RE IN THE DISRICHIE SOURCE DIRECTORY
:: Make sure pyinstaller is already installed otherwise it'll fail to package
echo Check: pyinstaller Modules
pyinstaller --version > NUL
if errorlevel 1 goto pyinstallerCheckFailed

:: Then start the packaging process
call :startPackage

:: Exit the script after
echo Done
goto:eof

:: Define some functions
:checkZipBuild
echo Check: Disrichie ZIP build

if NOT exists installer/files.zip (
	echo Error: No build of Disrichie has been made.
	echo
	echo Try to execute build.cmd or build-portable.cmd first and compress it into a ZIP file.
	echo 	After that, move it to the installer directory
)

goto:eof

:startPackage
echo Start: Build Installer
pyinstaller installer/main.py --name "disrichie-installer" --onefile --clean --noconfirm --noconsole ^
	--distpath "./dist/installer" --icon "../../assets/disrichie.ico" ^
	--path "./installer" --workpath "./dist/installer/build" ^
	--specpath "./dist/installer" --add-data "../../installer/files.zip;." ^
	--add-data "../../installer/header.png;." --add-data "../../installer/installer.ico;."
goto:eof

:pyinstallerCheckFailed
echo Error: pyinstaller is required for packaging disrichie into a binary executable, and is not installed.
echo Install it using: pip install pyinstaller
goto:eof