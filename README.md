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

# Building
Wanna build the standalone version for yourself so that your friends don't have to install Python? Let's go!

## Requirements
Disrichie requires the latest version of Python (or Python 3.10 at least) with the pip package manager.

And, if you don't have the required modules/packages installed, you can execute `tools/setupenv.cmd`

## The Final Instruction
Now, this could be very easy, execute this command:

```shell
$ ./tools/pack # You must be on the source directory to execute this, otherwise it'll fail!
```

To finally build the standalone version of Disrichie.

If that fails, you must go with the `python disrichie` stuff, sorry m8.

## Portable version (optional)
Do you want to show off Disrichie on your friends, with directly executing Disrichie immediately? Try out the portable version!

Just execute this command:

```shell
$ ./tools/pack-portable # You must be on the source directory in order to execute this!
```

Then it'll build the portable version of Disrichie executable.

Note that Disrichie will spawn a new window in order to display the current state of your Rich Presence availability (which is not present on the non-portable version), you can `--wait` to suppress this.

# FAQ
## UNIX support? (e.g Linux, macOS, FreeBSD)
Maybe soon, but I'm very busy and lazy to port Disrichie on another operating system.

If you managed to port it successfully, maybe I can put it on the releases page and I'll take you credit for making it possible.

## Why is this written in Python? Don't you write programs in C/C++ before?
Since I moved back to Windows 10 (or shall i say binbows 10 haha got em), It was so hard to setup a C/C++ workspace and I don't have time to choose whether I should use Visual Studio or MSYS2.

## Where can I contact the author?
You can either send a mail on `borcillofg2020@gmail.com` or chat in Discord: `GianXD#1059`

# Contribute
Contributing for Disrichie? You can do it anytime, on any file.

As long it's good and working, this will make Disrichie even function better!

### End of README.