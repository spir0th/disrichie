<h1 align="center">Disrichie</h1>

A simple program to display custom Rich Presence on Discord!

# Introduction
## So, what does this do?
Basically, it displays a custom Rich Presence status on your Discord account, don't worry it's not affiliated with Discord Inc.

## How do I get started?
If you wanna check it out immediately, or just want the standalone version, go to the [Releases](https://github.com/gianxddddd/disrichie/releases) page.

or, just do `git clone` for this repo (read the [Requirements](#requirements) section before proceeding) then execute `python disrichie`, this will run the main code using your Python interpreter directly.

# Running
## Requirements
Disrichie requires the latest version of Python (or Python 3.10 at least) with the pip package manager.

And, if you don't have the required modules/packages installed, you can execute the `tools/setupenv` script.

## Testing
Now that you have done all of the previous instructions, try to test Disrichie by executing:
```shell
$ python disrichie -h
```

And you'll be greeted with the help info.

# Examples
If you don't know how Disrichie works, let's try for an example:
```shell
$ disrichie -i 1013811673666158686
```

The `-i` option is where you put your client ID of your Application, you can create a new one at Discord's [Developer Portal](https://discord.com/developers/applications) and use it's client ID.

In your application, you can set the Rich Presence name there and upload the assets if you want to display images.

**The one used in the example is the ID from the `examples` directory.**

If you want more examples of this, read the help information, or if in easy way, use [Profiles](docs/PROFILES.md) instead. You can always find more profile examples at the `examples` directory.

# FAQ
## UNIX-like OS support? (e.g Linux, macOS, FreeBSD)
Partially supported.

## No GUI?
I'm actually quite lazy to do that, I would rather use Qt or tkinter but just can't do it because I'm busy.

## Why is this written in Python? Don't you write programs in C/C++ before?
Since I moved back to Windows 10, It was so hard to setup a C/C++ workspace and I don't have time to choose whether I should use Visual Studio or MSYS2.

# Contribute
Contributing for Disrichie? You can do it anytime, on any file.

As long it's good and working, this will make Disrichie even function better!

### End of README.