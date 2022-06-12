import appdirs
import os
from sys import exit
import sys
from tkinter.filedialog import askdirectory
from tkinter.font import Font
from tkinter.ttk import Progressbar
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from zipfile import ZipFile

try:
	from PIL import ImageTk, Image
except ModuleNotFoundError as error:
	raise RuntimeError(f"Failed to initialize installer: {error.msg}")

root: Tk = None
path: StringVar = None
extracting: bool = False

def resources_path() -> str:
	if not hasattr(sys, '_MEIPASS'): return ''
	return f"{sys._MEIPASS}/"

def init():
	global root, path
	if not root: root = Tk()
	if not path: path = StringVar(value=f"{appdirs.user_data_dir()}/disrichie")
	root.protocol('WM_DELETE_WINDOW', abort)
	root.iconbitmap(f"{resources_path()}installer.ico")
	root.title('Disrichie')
	root.resizable(False, False)
	center()

def ask_dir(path: str) -> str:
	new_path = askdirectory(initialdir=path if not path else None, mustexist=True)
	if not new_path: return path
	return new_path

def center():
	global root, path
	if not root and not path: raise RuntimeError('Installer has not yet fully initialized.')

	window_height = 500
	window_width = 500
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x_cordinate = int((screen_width / 2) - (window_width / 2))
	y_cordinate = int((screen_height / 2) - (window_height / 2))

	root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

def abort(loop_if_no: bool = False):
	global extracting
	if extracting: return
	response = messagebox.askyesno('Cancel', 'Do you want to exit installation?')

	if response: exit()
	elif not response:
		if loop_if_no: loop()
		else: pass

def fail(reason: str):
	global extracting
	if extracting: extracting = False
	messagebox.showerror('Installation error', reason)
	switch(5)

def clear():
	global root, path
	if not root and not path: raise RuntimeError('Installer has not yet fully initialized.')

	for widget in root.winfo_children():
		widget.destroy()

def switch(index: int = 0):
	global root, path, extracting
	if not root and not path: raise RuntimeError('Installer has not yet fully initialized.')
	if len(root.winfo_children()) > 0: clear()

	if index == 0: # Welcome screen
		# Create centered frame
		frame = Frame(root)
		frame.pack(expand=YES)

		# Create image header
		image = ImageTk.PhotoImage(Image.open(f"{resources_path()}header.png"))
		header = Label(frame, image=image)
		header.image = image
		header.pack(fill=X)

		# Create install button
		btn = Button(frame, text='Install', command=lambda: switch(1))
		btn.pack(fill=X)
	elif index == 1: # Destination and options screen
		# Create header
		header = Label(root, text='Destination Location')
		font = Font(font=header['font'])
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='Where do you want to install Disrichie?')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create destination entry and change button
		entry = Entry(root, width=50, textvariable=path)
		entry.pack(side=TOP, anchor=NW, padx=8, pady=24)
		btn_change = Button(root, text='Change...', command=lambda: path.set(ask_dir(path.get())))
		btn_change.pack(side=TOP, anchor=NW, padx=8)

		# Create navigation buttons
		btn_frame = Frame(root)
		btn_frame.pack(side=BOTTOM, anchor=E, padx=8, pady=8)
		btn = Button(btn_frame, text='Next', command=lambda: switch(2))
		btn.pack(in_=btn_frame, side=RIGHT)
		btn2 = Button(btn_frame, text='Go back', command=lambda: switch(0))
		btn2.pack(in_=btn_frame, side=RIGHT)
	elif index == 2: # Installation review screen
		# Create header
		header = Label(root, text='Review')
		font = Font(font=header['font'])
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create review message
		review = Message(root, width=400, text=f"Disrichie will be installed in {path.get()} "
			f"and it will take space of 17MB.")
		review.pack(side=TOP, anchor=NW, padx=8)

		# Create navigation buttons
		btn_frame = Frame(root)
		btn_frame.pack(side=BOTTOM, anchor=E, padx=8, pady=8)
		btn = Button(btn_frame, text='Proceed', command=lambda: switch(3))
		btn.pack(in_=btn_frame, side=RIGHT)
		btn2 = Button(btn_frame, text='Go back', command=lambda: switch(1))
		btn2.pack(in_=btn_frame, side=RIGHT)
	elif index == 3: # Installing page
		# Lock the exit button
		extracting = True

		# Create header
		header = Label(root, text='Installing')
		font = Font(font=header['font'])
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='Copying installation files, please wait...')
		text.pack(side=TOP, anchor=NW, padx=8, pady=16)

		# Create extraction filename text
		filename_text_str = StringVar(value='Initializing')
		filename_text = Label(root, textvariable=filename_text_str)
		filename_text.pack(side=TOP, anchor=NW, padx=8, pady=16)

		# Create extraction progress bar
		bar = Progressbar(orient=HORIZONTAL, length=500, mode='determinate', maximum=100, value=0)
		bar.pack(side=TOP, anchor=NW, padx=8)

		# Extract required files
		os.makedirs(path.get(), exist_ok=True)

		if not os.path.isfile(f"{resources_path()}files.zip"):
			filename_text_str.set('Error')
			fail('Missing installation files! Contact the author.')
			return

		zipfile = ZipFile(f"{resources_path()}files.zip")
		uncompressed_size = sum(file.file_size for file in zipfile.infolist())
		extract_size = 0

		for file in zipfile.infolist():
			extract_size += file.file_size
			filename_text_str.set(f"Extracting {file.filename()}")
			bar['value'] = extract_size * 100 / uncompressed_size
			zipfile.extract(file, path.get())
		
		# Finally close zipfile, and unlock the exit button, then switch to 4th screen
		zipfile.close()
		extracting = False
		switch(4)
	elif index == 4: # Installation success screen
		# Create header
		header = Label(root, text='Install success')
		font = Font(font=header['font'])
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='You may now exit this installation.')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create exit button
		btn = Button(root, text='Close', command=lambda: exit())
		btn.pack(side=BOTTOM, anchor=E, padx=8, pady=8)
	elif index == 5: # Failed to install screen
		# Create header
		header = Label(root, text='Failed to install')
		font = Font(font=header['font'])
		header.config(font=(font.actual(), 18))
		header.pack(side=TOP, anchor=NW, padx=8, pady=8)

		# Create text
		text = Label(root, text='An error occurred while setting up, you may now exit this installation.')
		text.pack(side=TOP, anchor=NW, padx=8)

		# Create exit button
		btn = Button(root, text='Close', command=lambda: exit(1))
		btn.pack(side=BOTTOM, anchor=E, padx=8, pady=8)

def loop():
	global root, path
	if not root and not path: raise RuntimeError('Installer has not yet fully initialized.')

	try:
		root.mainloop()
	except KeyboardInterrupt:
		abort(True)

init()
switch()
loop()