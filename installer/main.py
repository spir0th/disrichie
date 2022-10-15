try:
	import appdirs
except ModuleNotFoundError:
	raise RuntimeError('One of the required modules known as "appdirs" isn\'t installed.')

import os
import sys

try:
	from tkinter.filedialog import askdirectory
	from tkinter.font import Font
	from tkinter.ttk import Progressbar
	from tkinter import *
	from tkinter import messagebox
	from tkinter.ttk import *
except ModuleNotFoundError:
	raise RuntimeError('tkinter is not installed on your Python interpreter, '
		'see https://stackoverflow.com/a/25905642/16378482 if you\'re using UNIX-based OS')

from sys import exit
from zipfile import ZipFile

class InstallerInitError(Exception):
	def __init__(self):
		super().__init__('Installer has not yet fully initialized.')

root: Tk = None
path: StringVar = None
bypass: bool = False
verbose: bool = False
extracting: bool = False

def get_resource(path: str) -> str:
	# This function is necessary when it is built into an executable
	if not hasattr(sys, '_MEIPASS'): return path
	return f"{sys._MEIPASS}/{path}"

def init():
	global root, path
	if not root: root = Tk()
	if not path: path = StringVar(value=f"{appdirs.user_data_dir()}/disrichie")
	root.withdraw()
	root.protocol('WM_DELETE_WINDOW', abort)
	root.iconbitmap(get_resource("installer.ico"))
	root.title('Disrichie')
	root.resizable(False, False)
	resize_and_center()
	root.deiconify()

def ask_dir(path: str) -> str:
	ask_title = 'Choose a destination location'
	new_path = askdirectory(initialdir=path if not path else None, mustexist=True, title=ask_title)
	if not new_path: return path
	return new_path

def reset_dir():
	global path
	def_path = StringVar(value=f"{appdirs.user_data_dir()}/disrichie")
	path = def_path

def resize_and_center():
	global root
	if not root: raise InstallerInitError()

	window_height = 500
	window_width = 500
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x_coordinate = int((screen_width / 2) - (window_width / 2))
	y_coordinate = int((screen_height / 2) - (window_height / 2))
	
	root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

def abort(loop_if_no: bool = False):
	global extracting
	if extracting: return
	response = messagebox.askyesno('Cancel', 'Do you want to exit installation?')

	if response: exit()
	elif not response:
		if loop_if_no: loop()
		else: pass

def fail(reason: str):
	global extracting, verbose
	if extracting: extracting = False
	if verbose: print(f"Install failure: {reason}")
	messagebox.showerror('Installation error', reason)
	switch(4)

def clear():
	global root, verbose
	if not root: raise InstallerInitError()

	if verbose:
		print(f"Cleared {len(root.winfo_children())} children from UI stack.")
	for widget in root.winfo_children():
		widget.destroy()

def draw_separators():
	global root
	if not root: raise InstallerInitError()
	header_sep = Separator(root, orient=HORIZONTAL)
	navigation_sep = Separator(root, orient=HORIZONTAL)
	header_sep.place(relx=0, rely=0.15, relwidth=1, relheight=1)
	navigation_sep.place(relx=0, rely=0.92, relwidth=1, relheight=1)

def switch(index: int = 0):
	global root, path, extracting, bypass
	if not root and not path: raise InstallerInitError()
	if len(root.winfo_children()) > 0: clear()
	if index < 5: draw_separators()

	if index == 0: # Welcome screen
		# Create header
		header = Label(root, text='Welcome')
		font = Font(font=header['font'], weight='bold')
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='Disrichie will be installed by clicking "Install"'
			+ ' or configure location before installing.')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create navigation buttons
		btn_frame = Frame(root)
		btn_frame.pack(side=BOTTOM, anchor=E, padx=8, pady=8)
		btn = Button(btn_frame, text='Install', command=lambda: switch(2))
		btn.pack(in_=btn_frame, side=RIGHT)
		btn2 = Button(btn_frame, text='Exit', command=lambda: abort())
		btn2.pack(in_=btn_frame, side=RIGHT)
		btn3 = Button(btn_frame, text='Configure', command=lambda: switch(1))
		btn3.pack(in_=btn_frame, side=RIGHT)
	elif index == 1: # Destination screen
		# Create header
		header = Label(root, text='Destination Location')
		font = Font(font=header['font'], weight='bold')
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='Where do you want to install Disrichie?')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create destination entry and change button
		dest_frame = Frame(root)
		dest_frame.pack(side=TOP, anchor=NW, padx=8, pady=16)
		btn_change = Button(root, text='Change...', command=lambda: path.set(ask_dir(path.get())))
		btn_change.pack(in_=dest_frame, side=RIGHT, padx=8)
		entry = Entry(dest_frame, width=50, textvariable=path)
		entry.pack(in_=dest_frame, side=RIGHT)

		# Create navigation buttons
		btn_frame = Frame(root)
		btn_frame.pack(side=BOTTOM, anchor=E, padx=8, pady=8)
		btn = Button(btn_frame, text='Done', command=lambda: switch())
		btn.pack(in_=btn_frame, side=RIGHT)
		btn2 = Button(btn_frame, text='Cancel', command=lambda: [reset_dir(), switch()])
		btn2.pack(in_=btn_frame, side=RIGHT)
	elif index == 2: # Installing page
		# Lock the exit button
		extracting = True

		# Create header
		header = Label(root, text='Installing')
		font = Font(font=header['font'], weight='bold')
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='Copying installation files, please wait...')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create extraction status text
		status_text_str = StringVar(value='Initializing')
		status_text = Label(root, textvariable=status_text_str)
		status_text.pack(side=TOP, anchor=NW, padx=8, pady=16)

		# Create extraction progress bar
		bar = Progressbar(orient=HORIZONTAL, length=500, mode='determinate', maximum=100, value=0)
		bar.pack(side=TOP, anchor=NW, padx=8)

		# Extract required files
		files = get_resource("files.zip")

		if bypass:
			switch(3)
			extracting = False
			return
		if not os.path.isfile(files):
			status_text_str.set('Error')
			fail('Cannot find setup files.')
			return

		zipfile = ZipFile(files)
		uncompressed_size = sum(file.file_size for file in zipfile.infolist())
		os.makedirs(path.get(), exist_ok=True)
		extract_size = 0

		if verbose:
			print('Installing...')
		for file in zipfile.infolist():
			if verbose:
				print(f"Extracting {file.filename}")

			extract_size += file.file_size
			status_text_str.set('Copying new files')
			bar['value'] = extract_size * 100 / uncompressed_size
			zipfile.extract(file, path.get())
		
		# Close zipfile to save memory, unlock the exit button, then switch to 4th screen
		if verbose: print('Done')
		zipfile.close()
		extracting = False
		switch(3)
	elif index == 3: # Installation success screen
		# Create header
		header = Label(root, text='Installation successful')
		font = Font(font=header['font'], weight='bold')
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='You may now exit this installation.')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create exit button
		btn = Button(root, text='Close', command=lambda: exit())
		btn.pack(side=BOTTOM, anchor=E, padx=8, pady=8)
	elif index == 4: # Installation failed screen
		# Create header
		header = Label(root, text='Installation failed')
		font = Font(font=header['font'], weight='bold')
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='An error occurred while setting up, you may now exit this installation.')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create exit button
		btn = Button(root, text='Close', command=lambda: exit(1))
		btn.pack(side=BOTTOM, anchor=E, padx=8, pady=8)

def parse_args():
	global root, path, bypass, verbose
	args = sys.argv[1:]

	for index, argument in enumerate(args):
		if argument == '-h' or argument == '--help':
			print('-h / --h : View help information')
			print('-o / --output : Set output path for extract')
			print('-v / --verbose : Enable verbose logging')
			print('--bypass : Skip installation, used for testing purposes')
		if len(args) > index + 1:
			continue
		if argument == '--bypass':
			bypass = True
		if argument == '-o' or argument == '--output':
			path = StringVar(root, args[index + 1])
		if argument == '-v' or argument == '--verbose':
			print('Verbose logging is enabled.')
			verbose = True

def loop():
	global root
	if not root: raise InstallerInitError()

	try:
		root.mainloop()
	except KeyboardInterrupt:
		abort(True)

try:
	init()
except TclError as error:
	if error.args[0] == 'no display name and no $DISPLAY environment variable':
		print('GUI in your environment is not supported.')
		exit(1)
	else: pass

parse_args()
switch()
loop()