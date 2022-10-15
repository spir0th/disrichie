# Standalone Version
## What is it?
Disrichie runs on an interpreter, and requires Python to be installed.

The Standalone Version, however makes it easier by using [PyInstaller](https://pyinstaller.org) to convert it into a binary executable. This version will not require you to install Python.

## Building
Execute this command:
```shell
$ ./tools/build # You must be on the source directory to execute this, otherwise it'll fail!
```

to build the project into standalone.

### Installer (optional)
If you also want to build the installer, you must check the following needs before you can execute `tools/build-installer`:

- Has already built a standalone version and put into the installer directory in a compressed ZIP file called `files.zip`
- Cleaned the `dist` directory

Once you have done the needed, you can now execute `tools/build-installer`, still noted that you must be on the source directory when you do it.