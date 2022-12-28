### Imports ###
from __future__ import annotations # very damas

import datetime
import json
import os
import platform
import signal
import subprocess
import sys
import tempfile
import time

from sys import executable
from sys import exit

try:
	from pypresence import DiscordError
	from pypresence import DiscordNotFound
	from pypresence import Presence as DiscordRPC
except ModuleNotFoundError:
	raise RuntimeError('Could not find a proper Discord Rich Presence library.') from None

### Exceptions ###
class ProfileNotFoundError(Exception):
	"""Profile not found error. Mostly caused by nonexisting or missing profile."""
	def __init__(self):
		super().__init__('Specified profile not found or is not available.')

class ProfileParseError(Exception):
	"""Profile parsing error. Mostly caused by raw data being corrupted or not formatted correctly."""
	def __init__(self):
		super().__init__('Failed to parse profile. Raw data might be corrupted.')

class ClientIDSyntaxError(Exception):
	"""Client ID syntax error. It should not contain alphabetical or special characters."""
	def __init__(self):
		super().__init__('Client IDs should not contain alphabetical or special characters.')

class TooMuchButtonsError(Exception):
	"""Too much buttons on profile error. Remove unnecessary buttons on the raw data."""
	def __init__(self):
		super().__init__('There are too many buttons defined on profile.')

### Process utilities ###
lockfile_path = f"{tempfile.gettempdir()}/driprichie.lock" # so drip

def is_locked() -> bool:
	"""Returns true if Disrichie is locked for another instance."""
	return os.path.isfile(lockfile_path)

def lockfile_pid() -> int:
	"""Get the process id of the locked Disrichie instance."""
	if not is_locked():
		print('No lockfile exists, cannot get locked process ID.')
		return 0
	
	lockfile = open(lockfile_path, 'r')
	pid = lockfile.readline()
	lockfile.close()
	return int(pid)

def init_lockfile():
	"""Locks this Disrichie instance, so that only one instance can run at once."""
	lockfile = open(lockfile_path, 'w')
	lockfile.write(str(os.getpid()))
	lockfile.close()

def destroy_lockfile():
	"""Unlocks this Disrichie instance, and other instances can be ran."""
	if not is_locked():
		print('Lockfile has already been deleted.')
		return
	
	try:
		os.remove(lockfile_path)
	except FileNotFoundError:
		print('Cannot delete lockfile, maybe removed or missing?')

def is_standalone() -> bool:
	"""Returns true if script is running as a standalone program, otherwise false."""
	return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

### Profile ###
# For more info about profiles, read the "PROFILES.md" file from the "docs" directory
class Profile:
	"""The class which stores the data of a Disrichie profile."""
	path = None
	data = None

	def __init__(self, path: str = '{}'):
		self.path = path
		self.parse()
		self.validate()
	
	def parse(self):
		"""Parse the raw data of this profile by reading the file using path.
		
		If path is unspecified, then it will throw a ProfileParseError.
		"""
		if self.path != '{}':
			if self.path == None or not os.path.isfile(self.path):
				raise ProfileNotFoundError()
			
			file = open(self.path, 'r')

		try:
			if self.path != '{}': self.data = json.load(file)
			else: self.data = json.loads(self.path) # Load empty JSON if path is unset
		except json.JSONDecodeError:
			raise ProfileParseError()

		if self.path != '{}': file.close()
	
	def validate(self):
		"""Validates the parsed data.
		
		If parsed data is invalid, then it will throw a ProfileParseError.
		"""
		if self.data == None: raise ProfileParseError()

	def client_id(self) -> int:
		"""Returns the client ID set on this profile."""
		if 'clientId' not in self.data or \
			not isinstance(self.data['clientId'], int) or \
			not self.data['clientId']: return 0
		
		return int(self.data['clientId'])

	def details(self) -> str:
		"""Returns the details text of this profile."""
		if 'details' not in self.data or \
			not isinstance(self.data['details'], str) or \
			not self.data['details']: return None
		return str(self.data['details'])

	def state(self) -> str:
		"""Returns the state text of this profile."""
		if 'state' not in self.data or \
			not isinstance(self.data['state'], str) or \
			not self.data['state']: return None
		return str(self.data['state'])
	
	def elapsed(self) -> float:
		"""Returns the elapsed time of this profile if enabled."""
		if 'elapsed' not in self.data or \
			not isinstance(self.data['elapsed'], bool) or \
			not self.data['elapsed']: return None
		
		return float(datetime.datetime.now().timestamp())

	def large_image_key(self) -> str:
		"""Returns the asset key of large image on this profile."""
		if 'largeImageKey' not in self.data or \
			not isinstance(self.data['largeImageKey'], str) or \
			not self.data['largeImageKey']: return None
		
		return str(self.data['largeImageKey'])

	def small_image_key(self) -> str:
		"""Returns the asset key of small image on this profile."""
		if 'smallImageKey' not in self.data or \
			not isinstance(self.data['smallImageKey'], str) or \
			not self.data['smallImageKey']: return None
		
		return str(self.data['smallImageKey'])

	def large_image_text(self) -> str:
		"""Returns the caption/text of large image on this profile."""
		if 'largeImageText' not in self.data or \
			not isinstance(self.data['largeImageText'], str) or \
			not self.data['largeImageText']: return None
		
		return str(self.data['largeImageText'])
	
	def small_image_text(self) -> str:
		"""Returns the caption/text of small image on this profile."""
		if 'smallImageText' not in self.data or \
			not isinstance(self.data['smallImageText'], str) or \
			not self.data['smallImageText']: return None
		
		return str(self.data['smallImageText'])
	
	def buttons(self) -> list[dict]:
		"""Returns a list of buttons set on this profile. """
		if 'buttons' not in self.data or \
			len(self.data['buttons']) < 1: return None
		for button in self.data['buttons']:
			if 'label' not in button or not button['label'] or \
				'url' not in button or not button['url'] or \
					len(button) < 1:
				self.data['buttons'].remove(button)
				continue

		return list[dict](self.data['buttons'])

### Main Class ###
class Disrichie:
	"""The main class of Disrichie, used for displaying Rich Presence with custom info."""
	dont_wait: bool = True # Must spawn a background process unless the --wait option is appended
	client_id: int = 0 # Required to be set from the command-line or the profile
	profile: Profile = Profile() # Load with no keys
	rpc: DiscordRPC = None # Base RPC instance should be set to None
	running: bool = False # Set running to false by default

	def __init__(self, args: list[str], profile_path: str = None):
		if sys.version_info[1] < 7:
			raise RuntimeError("Python 3.6.15 or greater is required.")
		if profile_path != None:
			self.init_profile(profile_path)
		
		self.args: list[str] = args
		self.parse_args()

	def __del__(self):
		self.stop()

	def parse_args(self):
		"""Parses arguments passed from the constructor, will be called automatically constructed."""
		arguments: list[str] = ['-i', '--id', '-d',
			'--details', '-s', '--state', '--elapsed',
			'--large-image-key', '--large-image-text',
			'--small-image-key', '--small-image-text']
		options: list[str] = ['--cancel', '--cache', '-h',
			'--help', '--tracebacks',
			'-v', '--version', '--wait']

		for index, argument in enumerate(self.args):
			if index == 0 and \
				argument not in arguments and \
					argument not in options:
					self.init_profile(argument)

			if len(self.args) < index + 1:
				continue
			if argument == "-i" or argument == "--id":
				self.client_id = self.args[index + 1]
			if argument == "-d" or argument == "--details":
				self.profile.data["details"] = self.args[index + 1]
			if argument == "-s" or argument == "--state":
				self.profile.data["state"] = self.args[index + 1]
			if argument == "--elapsed":
				self.profile.data["elapsed"] = self.args[index + 1]
			if argument == "--large-image-key":
				self.profile.data["largeImageKey"] = self.args[index + 1]
			if argument == "--large-image-text":
				self.profile.data["largeImageText"] = self.args[index + 1]
			if argument == "--small-image-key":
				self.profile.data["smallImageKey"] = self.args[index + 1]
			if argument == "--small-image-text":
				self.profile.data["smallImageText"] = self.args[index + 1]
		for option in options:
			if option not in self.args:
				continue
			if option == '--cache':
				sys.dont_write_bytecode = True
			if option == '--cancel':
				if not self.kill_instance():
					print('No background processes are running.')

				exit()
			if option == '-h' or option == '--help':
				program = "program" if is_standalone() else "script"
				print(f"disrichie - A simple {program} to display custom Rich Presence on Discord!")
				print('\nArguments:')
				print('	--cache : Enable caching for this instance')
				print('	--cancel : Tells the locked instance to stop showing Rich Presence')
				print('	-h / --help : Display help information')
				print('	--tracebacks : Print not only the error but from where it was fired')
				print(f"	-v / --version : Print {program} version")
				print('	--wait : Do not put instance into background and wait for user')
				print('\nRich Presence arguments:')
				print('	-i / --id : Client ID to be used for this Rich Presence')
				print('	-d / --details : Used to display below the Rich Presence name')
				print('	-s / --state : Used to display below the details')
				print('	--elapsed : Shows the elapsed time if set')
				print('	--large-image-key : Shows the big image from the client ID')
				print('	--small-image-key : Shows the small image from the client ID')
				print('	--large-image-text : Displayed when the big image is hovered')
				print('	--small-image-key : Displayed when the small image is hovered')
				exit()
			if option == '--tracebacks':
				sys.tracebacklimit = 0
			if option == '-v' or option == '--version':
				print('version 1.0.5')
				exit()
			if option == '--wait':
				self.dont_wait = False

	def kill_instance(self, failsafe: bool = True) -> bool:
		"""Kills locked instance, automatically called when RPC is started."""
		if not is_locked():
			return False
		
		try:
			pid = lockfile_pid()
			os.kill(pid, signal.SIGINT)
			print(f"Killed background process {pid}")
		except:
			print("Unable to kill background process, deleting lockfile to finalize...")
			destroy_lockfile()

			if is_locked():
				print('Cannot delete lockfile either, is it missing or removed?')
				if not failsafe: exit()

			return False

		return True

	def spawn_background(self):
		"""Spawns another Disrichie instance in background, which can be killed by
		using the kill_instance function.
		"""
		# In order to spawn Disrichie in the background
		# We must append the option --wait to avoid spawn iteration (looping processes)
		argv = self.args
		exec = [executable, __file__]

		if is_standalone():
			exec = [executable]
		if '--wait' not in argv:
			argv.append('--wait')
		if platform.system() == 'Windows':
			subprocess.Popen(args=exec + argv,
				creationflags=subprocess.DETACHED_PROCESS)
		else:
			subprocess.Popen(args=exec + argv,
				stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	def init_profile(self, path: str):
		"""Initialize profile from path."""
		self.profile = Profile(path)
		self.client_id = self.profile.client_id()

	def stop(self):
		"""Stops running RPC instance."""
		if self.running and self.rpc: self.rpc.clear()
		if is_locked(): destroy_lockfile()
		self.running = False

	def start(self):
		"""Starts RPC instance."""
		self.kill_instance(True)
		init_lockfile()

		if not self.client_id:
			print('No client ID has been set. See help for more information.')
			return
		if self.dont_wait:
			self.spawn_background()
			return

		try:
			self.rpc = DiscordRPC(str(self.client_id))
			self.rpc.connect()
		except KeyboardInterrupt:
			# Interruption was caught during initialization, so do nothing instead
			return
		except DiscordError as error:
			print(error.message)
			return
		except DiscordNotFound:
			print('Discord is not running or installed.')
			return

		self.rpc.update(details=self.profile.details(), state=self.profile.state(),
			start=self.profile.elapsed(),
			large_image=self.profile.large_image_key(), small_image=self.profile.small_image_key(),
			large_text=self.profile.large_image_text(), small_text=self.profile.small_image_text(),
			buttons=self.profile.buttons())

		self.running = True
		print('Rich Presence is now visible.')
		self.wait()

	def wait(self):
		"""Wait for user to stop RPC instance, called by the start function."""
		try:
			while self.running: time.sleep(15)
		except KeyboardInterrupt:
			pass

### Main process will run if script is ran as program or directly from interpreter ###
if __name__ == "__main__":
	instance = Disrichie(sys.argv[1:])
	instance.start()