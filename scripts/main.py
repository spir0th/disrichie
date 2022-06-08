import os

try:
	from errors import *
	from process import *
	from pypresence import DiscordNotFound
	from pypresence import Presence
except ModuleNotFoundError:
	raise ModuleNotFoundError('Unable to find the required modules,'
								' make sure Disrichie is configured properly.')

import signal
from sys import exit
import time

if __name__ == '__main__':
	raise RuntimeError('Disrichie must be ran from the launcher script.')

class Disrichie:
	client_id: int = 0 # Required to be set from the command-line
	running: bool = False

	def __init__(self, args: list[str]):
		self.args: list[str] = args
		self.parse_args()

	def parse_args(self):
		options: list[str] = ['--cancel']

		for index, argument in enumerate(self.args):
			if argument == "--id" or argument == "--client-id" and \
				len(self.args) > index + 1 and \
					self.args[index + 1] not in options:
				self.client_id = self.args[index + 1]

		for option in options:
			if option not in self.args: continue
			if option == '--cancel':
				self.kill_oinstance()
				exit()

	def kill_oinstance(self, exit_on_fail: bool = False):
		if not is_locked():
			return
		
		try:
			pid = lockfile_pid()
			os.kill(pid, signal.SIGINT)
			print(f"Killed Disrichie process {pid}")
		except:
			print('Unable to kill another instance, maybe it was forcefully killed?')
			if exit_on_fail: exit()

	def cancel(self):
		destroy_lockfile()
		self.running = False
	
	def start_rpc(self):
		self.kill_oinstance(True)
		init_lockfile()
		
		if not self.client_id:
			print('No client ID has been set. See help for more information.')
			return
		
		rpc: Presence = None

		try:
			rpc = Presence(str(self.client_id))
		except DiscordNotFound:
			print('Discord is not running or installed.')
			return

		rpc.connect()
		rpc.update(state='deez nuts')
		print('Rich Presence is now visible!')
		self.running = True

		try:
			while self.running:
				time.sleep(15)
		except KeyboardInterrupt:
			exit()

