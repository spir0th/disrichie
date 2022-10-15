from __future__ import annotations
import datetime
from errors import ProfileInvalidationError
from errors import ProfileParseError
import json

class Profile:
	path: str = None
	data = None

	def __init__(self, path: str = '{}'):
		self.path = path
		self.parse()
		self.invalidate()
	
	def parse(self):
		if self.path == None: raise ProfileParseError()
		if self.path != '{}': file = open(self.path, 'r')

		try:
			if self.path != '{}': self.data = json.load(file)
			else: self.data = json.loads(self.path) # Load empty JSON
		except json.JSONDecodeError:
			raise ProfileParseError()

		if self.path != '{}': file.close()
	
	def invalidate(self):
		if self.data == None: raise ProfileInvalidationError()

	def client_id(self) -> int:
		if 'clientId' not in self.data or \
			not isinstance(self.data['clientId'], int) or \
			not self.data['clientId']: return 0
		
		return int(self.data['clientId'])

	def details(self) -> str:
		if 'details' not in self.data or \
			not isinstance(self.data['details'], str) or \
			not self.data['details']: return None
		return str(self.data['details'])

	def state(self) -> str:
		if 'state' not in self.data or \
			not isinstance(self.data['state'], str) or \
			not self.data['state']: return None
		return str(self.data['state'])
	
	def elapsed(self) -> float:
		if 'elapsed' not in self.data or \
			not isinstance(self.data['elapsed'], bool) or \
			not self.data['elapsed']: return None
		
		return float(datetime.datetime.now().timestamp())

	def large_image_key(self) -> str:
		if 'largeImageKey' not in self.data or \
			not isinstance(self.data['largeImageKey'], str) or \
			not self.data['largeImageKey']: return None
		
		return str(self.data['largeImageKey'])

	def small_image_key(self) -> str:
		if 'smallImageKey' not in self.data or \
			not isinstance(self.data['smallImageKey'], str) or \
			not self.data['smallImageKey']: return None
		
		return str(self.data['smallImageKey'])

	def large_image_text(self) -> str:
		if 'largeImageText' not in self.data or \
			not isinstance(self.data['largeImageText'], str) or \
			not self.data['largeImageText']: return None
		
		return str(self.data['largeImageText'])
	
	def small_image_text(self) -> str:
		if 'smallImageText' not in self.data or \
			not isinstance(self.data['smallImageText'], str) or \
			not self.data['smallImageText']: return None
		
		return str(self.data['smallImageText'])
	
	def buttons(self) -> list[dict]:
		if 'buttons' not in self.data or \
			len(self.data['buttons']) < 1: return None
		for button in self.data['buttons']:
			if 'label' not in button or not button['label'] or \
				'url' not in button or not button['url'] or \
					len(button) < 1:
				self.data['buttons'].remove(button)
				continue

		return list[dict](self.data['buttons'])