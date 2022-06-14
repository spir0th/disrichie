<h1 align="center">Disrichie</h1>

A simple program to display custom Rich Presence on Discord!

# Introduction
## So, what the hell does this do?
Basically, it displays a custom Rich Presence status on your Discord account, don't worry it's not affiliated with Discord Inc.

## Will I get banned from Discord when I use this?
No, it does not violate Discord's Terms of Service. It's not like you're modifying the Discord webapp itself.

## How do I get started?
If you wanna check it out immediately, or just want the standalone version, go to the [Releases](https://github.com/gianxddddd/disrichie/releases) page.

or, just do `git clone` for this repo then execute `python disrichie` (This runs disrichie from your Python interpreter)

# Building & Running
## Requirements
Disrichie requires the latest version of Python (or Python 3.10 at least) with the pip package manager.

And, if you don't have the required modules/packages installed, you can execute `tools/setupenv.cmd`

## Getting Discord GameSDK
As of commit [3176621](https://github.com/gianxddddd/disrichie/commit/31766212290f029a9ff8c3f4ff26e92926197303), Disrichie now uses Discord GameSDK by default (instead of the old Discord-RPC)

In order to run Disrichie right now is to get the required GameSDK libraries.

- Get it [here.](https://dl-game-sdk.discordapp.net/2.5.6/discord_game_sdk.zip)
- Extract it and copy `lib/x86_64/discord_game_sdk.dll` to `disrichie/lib`
	- Library files might differ, for example:
		- `discord_game_sdk.so` for UNIX-like OSes

If you tend to use the legacy library (Discord-RPC), you still need to do these steps because `main.py` does not have the ability to optionally import the GameSDK modules.

## Running
Now that you have done all of the previous instructions, you can now run Disrichie by executing: `python disrichie -h`

```shell
> python disrichie -h
disrichie - A simple program to display custom Rich Presence on Discord!

Arguments:
        -p / --profile : Specify Rich Presence profile
        -i / --id : Specify Client ID for Rich Presence
        --wait : Do not put Disrichie into background and wait to end        
        --legacy : Use the old Discord-RPC library instead of Discord GameSDK

Launcher arguments:
        -h / --help : Display help information
        -v / --version : Print program version
        --cache : Enable caching for this instance
        --tracebacks : Print not only the error but from where it was fired
```

## Building the Standalone version (optional)
To build the standalone version, execute this command:
```shell
$ ./tools/build # You must be on the source directory to execute this, otherwise it'll fail!
```

then it will build the Standalone version.

## Building the Installer (optional)
If you want to build the installer by yourself, you must check the following needs before you can execute `tools/build-installer.cmd`:

- Has already built a standalone version and put into the installer directory in a compressed ZIP file called `files`
- Cleaned the `dist` directory

Once you have done the needed, you can now execute `tools/build-installer.cmd`, still noted that you must be on the source directory when you do it.

Note: This only works on the Standalone version and not the portable one.

# FAQ
## Why the Portable version was removed?
Since GameSDK was added and set as the default Rich Presence library, the Portable version was a bit.. Problematic. Yes, it was throwing errors that it couldn't find the library file.

So I tried so hard, but none of my fixes did work and I don't have much time left fixing it, so I gave up, removed the build scripts related to the Portable version, then wrote this question & answer.

## UNIX-like OS support? (e.g Linux, macOS, FreeBSD)
Partially supported.

If you managed to port it completely, maybe I can put it on the releases page and I'll take you credit for making it possible.

## No GUI?
I'm actually quite lazy to do that, I would rather use Qt or tkinter (yes the gui library that i used for the installer, but i did it during my freetime) but just can't do it because I'm busy.

## Why is this written in Python? Don't you write programs in C/C++ before?
Since I moved back to Windows 10 (or shall i say binbows 10 haha got em), It was so hard to setup a C/C++ workspace and I don't have time to choose whether I should use Visual Studio or MSYS2.

## Where can I contact the author?
You can either send a mail on `borcillofg2020@gmail.com` or chat in Discord: `GianXD#1059`

# Contribute
Contributing for Disrichie? You can do it anytime, on any file.

As long it's good and working, this will make Disrichie even function better!

### End of README.