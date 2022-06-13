from __future__ import annotations

try:
	from errors import *
	from process import *
	from profile import DisrichieProfile
	from pypresence import DiscordError
	from pypresence import DiscordNotFound
	from pypresence import Presence
except ModuleNotFoundError:
	raise ModuleNotFoundError('Unable to find the required modules,'
								' make sure Disrichie is configured properly.')

import os
import platform
import re
import signal
import subprocess
from sys import executable
from sys import exit
import time

if __name__ == '__main__':
	raise RuntimeError('Disrichie must be ran from the launcher script.')

class Disrichie:
	dont_wait: bool = True # Must spawn a background process unless the --wait option is appended
	client_id: int = 0 # Required to be set from the command-line
	profile: DisrichieProfile = DisrichieProfile() # Load with no keys
	rpc: Presence = None
	running: bool = False

	def __init__(self, args: list[str]):
		self.args: list[str] = args
		self.parse_args()

	def __del__(self):
		self.stop()

	def parse_args(self):
		options: list[str] = ['--cancel', '--wait']

		for index, argument in enumerate(self.args):
			if argument == "-i" or argument == "--id" and \
				len(self.args) > index + 1 and \
					self.args[index + 1] not in options:
				self.init_client_id(self.args[index + 1])
			if argument == "-p" or argument == "--profile" and \
				len(self.args) > index + 1 and \
					self.args[index + 1] not in options:
				self.init_profile(self.args[index + 1])

		for option in options:
			if option not in self.args: continue
			if option == '--cancel':
				if not self.kill_instance():
					print('No background processes are running')

				exit()
			if option == '--wait':
				self.dont_wait = False

	def kill_instance(self, exit_on_fail: bool = False) -> bool:
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
				print('Cannot delete lockfile either, must be already removed unexpectedly?')
				if exit_on_fail: exit()

			return False

		return True

	def spawn_background(self):
		# In order to spawn Disrichie in the background
		# We must append the option --wait to avoid spawn iteration (looping processes)
		argv = self.args
		if '--wait' not in argv: argv.append('--wait')
		print('Rich Presence will be visible soon.')

		if platform.system() == 'Windows':
			subprocess.Popen(args=[executable, 'disrichie'] + argv, creationflags=subprocess.DETACHED_PROCESS)
		else:
			subprocess.Popen(args=[executable, 'disrichie'] + argv,
				stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	def init_client_id(self, id: str):
		if os.path.isfile(id):
			file = open(id, 'r')
			self.client_id = file.readline()
			file.close()
			return
		if any(char.isalpha() for char in id) or \
			re.compile('[@_!#$%^&*()<>?/\|}{~:]').search(id) != None:
			raise ClientIDSyntaxError()
		
		self.client_id = int(id)

	def init_profile(self, path: str):
		if not os.path.isfile(path): raise ProfileNotFoundError()
		self.profile = DisrichieProfile(path)

	def stop(self):
		if self.rpc: self.rpc.clear()
		if is_locked(): destroy_lockfile()
		self.running = False

	def start(self):
		self.kill_instance(True)
		init_lockfile()
		
		if not self.client_id:
			print('No client ID has been set. See help for more information.')
			return
		if self.dont_wait:
			self.spawn_background()
			return

		try:
			self.rpc = Presence(client_id=str(self.client_id))
			self.rpc.connect()
		except DiscordError as error:
			print(error.message)
			return
		except DiscordNotFound:
			print('Discord is not running or installed')
			return

		self.rpc.update(state=self.profile.state(), details=self.profile.details(),
			start=self.profile.start_timestamp(),
			large_image=self.profile.large_image(), small_image=self.profile.small_image(),
			large_text=self.profile.large_image_text(), small_text=self.profile.small_image_text(),
			buttons=self.profile.buttons())
		print('Rich Presence is now visible!')
		self.running = True
		self.wait()

	def wait(self):
		try:
			while self.running:
				time.sleep(15)
		except KeyboardInterrupt:
			pass