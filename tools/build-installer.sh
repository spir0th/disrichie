# build-installer.sh - UNIX wrapper for the build-installer.cmd script
# ONLY EXECUTE THIS WHEN YOU'RE IN THE DISRICHIE SOURCE DIRECTORY
# Define some functions
checkZipBuild() {
	echo "Check: Disrichie ZIP build"

	if [ ! -f installer/files.zip ]; then
		echo Error: No build of Disrichie has been made.
		echo Try to execute build.cmd or build-portable.cmd first and compress it into a ZIP file.
		echo After that, move it to the installer directory
		exit 1
	fi
}

startPackage() {
	echo "Start: Build Installer"
	pyinstaller installer/main.py --name "installer" --onefile --clean --noconfirm --noconsole \
		--distpath "./dist/installer" --path "./installer" \
		--workpath "./dist/installer/build" --specpath "./dist/installer" \
		--add-data "../../installer/files.zip:." --add-data "../../installer/header.png:." \
		--add-data "../../installer/installer.ico:."
}

pyinstallerCheckFailed() {
	echo "Error: pyinstaller is required for packaging the Installer into a binary executable, and is not installed."
	echo "Install it using: pip install pyinstaller"
	exit 1
}

# Make sure pyinstaller is already installed otherwise it'll fail to package
echo "Check: pyinstaller"

if ! command -v "pyinstaller" &>/dev/null
then
	pyinstallerCheckFailed
fi

# Then call the process functions
checkZipBuild
startPackage

# Exit the script after
echo Done