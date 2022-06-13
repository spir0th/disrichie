# build.sh - UNIX wrapper for the build.cmd script
# ONLY EXECUTE THIS WHEN YOU'RE IN THE DISRICHIE SOURCE DIRECTORY
# Define some functions
startPackage() {
	echo "Start: Build Standalone version"
	pyinstaller disrichie --clean --noconfirm \
		--path "./scripts" --workpath "./dist/build" \
		--specpath "./dist" --version-file "../assets/version_info.txt"
}

pyinstallerCheckFailed() {
	echo "Error: pyinstaller is required for packaging disrichie into a binary executable, and is not installed."
	echo "Install it using: pip install pyinstaller"
	exit 1
}

# Make sure pyinstaller is already installed otherwise it'll fail to package
echo "Check: pyinstaller"

if ! command -v "pyinstaller" &>/dev/null
then
	pyinstallerCheckFailed
fi

# Then start the packaging process=
startPackage

# Exit the script after
echo "Done"