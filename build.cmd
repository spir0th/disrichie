:: build.cmd - Build script for Windows
@echo off

call :validateModules
call :cleanBuild
call :processBuild
goto:eof

:validateModules
cmd /k "tools\setupenv.cmd && exit"
goto:eof

:cleanBuild
cmd /k "tools\cleandist.cmd && exit"
goto:eof

:processBuild
pyinstaller disrichie.py --onefile --noconfirm ^
	--icon "../assets/disrichie.ico" --workpath "dist/build" ^
	--specpath "dist" ^ --version-file "../assets/version_info.txt"
goto:eof