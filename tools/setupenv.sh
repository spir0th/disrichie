# setupenv.sh - UNIX wrapper for the setupenv.cmd script
# Define some error functions
py_check_failed() {
	echo "Error: Python 3 is required to run disrichie for interpreted run, but is not installed."
	exit 1
}

pip_check_failed() {
	echo "Error: pip is required to install required modules/packages for disrichie, and is not installed."
	exit 1
}

# Check if Python 3 is installed
echo "Check: Python 3"

if ! command -v "python3" &>/dev/null
then
	py_check_failed
fi

# Also for pip
echo "Check: PIP"

if ! command -v "pip" &>/dev/null
then
	pip_check_failed
fi

# Install required modules
echo "Install: Required Modules"
pip install pypresence appdirs pillow

# Then exit the script
echo "Done"