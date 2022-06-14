class ProfileNotFoundError(Exception):
	def __init__(self):
		super().__init__('Specified profile not found')

class ProfileParseError(Exception):
	def __init__(self):
		super().__init__('Profile failed to parse')

class ProfileInvalidationError(Exception):
	def __init__(self, key: str = None):
		if not key:
			super().__init__('Profile invalidation error')
			return

		super().__init__(f"Failed to invalidate profile because {key} wasn't defined")

class TooMuchButtonsError(Exception):
	def __init__(self):
		super().__init__('There are too many buttons defined on the specified profile')

class ClientIDSyntaxError(Exception):
	def __init__(self):
		super().__init__('Check if the specified Client ID has no alphabetical and special characters')