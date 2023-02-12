# setupenv.sh - A script that installs required modules for Disrichie
py_check_failed() {
	echo "Error: Python 3 is not installed."
	exit 1
}

pip_check_failed() {
	echo "Error: pip is not installed. Refer to Python Manuals for installation."
	exit 1
}

# Check if Python 3 is installed
if ! command -v "python3" &>/dev/null
then
	py_check_failed
fi

# Also for pip
if ! command -v "pip" &>/dev/null
then
	pip_check_failed
fi

# Install required modules
pip install pypresence pyinstaller