class NoRichPresenceLibraryError(Exception):
	def __init__(self):
		super().__init__('No Rich Presence library was specified.')

class RichPresenceLibraryError(Exception):
	def __init__(self, library: int):
		library_name = "";

		if library == 0:
			library_name = "Discord RPC";
		elif library == 1:
			library_name = "GameSDK";
		if library_name == "":
			raise NoRichPresenceLibraryError()

		super().__init__(f"{library_name} failed to initialize.")