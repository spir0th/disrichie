import datetime
from errors import ProfileInvalidationError
from errors import ProfileParseError
import json

class DisrichieProfile:
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

	def details(self) -> str:
		if 'details' not in self.data: return None
		return self.data['details']

	def state(self) -> str:
		if 'state' not in self.data: return None
		return self.data['state']
	
	def start_timestamp(self) -> float:
		if 'displayElapsed' not in self.data or \
			not self.data['displayElapsed']: return None
		
		return datetime.datetime.now().timestamp()

	def large_image(self) -> str:
		if 'largeImage' not in self.data: return None
		return self.data['largeImage']

	def small_image(self) -> str:
		if 'smallImage' not in self.data: return None
		return self.data['smallImage']

	def large_image_text(self) -> str:
		if 'largeImageText' not in self.data: return None
		return self.data['largeImageText']
	
	def small_image_text(self) -> str:
		if 'smallImageText' not in self.data: return None
		return self.data['smallImageText']