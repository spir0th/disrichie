# Standalone Version
## What is it?
Disrichie is a Python project, which only runs on it's own interpreter, which makes it useless.

The Standalone Version, instead, makes it easier by using [PyInstaller](https://pyinstaller.org) to convert it into a binary executable.

## Building
Execute this command:
```shell
$ ./tools/build # You must be on the source directory to execute this, otherwise it'll fail!
```

then it produces the Standalone Version.

### Installer (optional)
If you also want to build the installer, you must check the following needs before you can execute `tools/build-installer`:

- Has already built a standalone version and put into the installer directory in a compressed ZIP file called `files.zip`
- Cleaned the `dist` directory

Once you have done the needed, you can now execute `tools/build-installer`, still noted that you must be on the source directory when you do it.

## Is it better than the normal version?
For most people who don't know programming, yes.

Without this, you are forced to install Python and Disrichie's require modules using `pip`, and it can be pain if you get errors.