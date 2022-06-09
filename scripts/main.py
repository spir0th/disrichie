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
import re
import signal
from sys import exit
import time

if __name__ == '__main__':
	raise RuntimeError('Disrichie must be ran from the launcher script.')

class Disrichie:
	client_id: int = 0 # Required to be set from the command-line
	profile: DisrichieProfile = DisrichieProfile() # Load with no keys
	rpc: Presence = None
	running: bool = False

	def __init__(self, args: list[str]):
		self.args: list[str] = args
		self.parse_args()

	def parse_args(self):
		options: list[str] = ['--cancel']

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
				self.kill_instance()
				exit()

	def kill_instance(self, exit_on_fail: bool = False):
		if not is_locked():
			return
		
		try:
			pid = lockfile_pid()
			os.kill(pid, signal.SIGINT)
			print(f"Killed Disrichie process {pid}")
		except:
			print('Unable to kill another instance, maybe it was forcefully killed?')
			if exit_on_fail: exit()

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

	def cancel(self):
		if self.rpc:
			self.rpc.clear()

		destroy_lockfile()
		self.running = False
	
	def start(self):
		self.kill_instance(True)
		init_lockfile()
		
		if not self.client_id:
			print('No client ID has been set. See help for more information.')
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
			self.cancel()
			exit()