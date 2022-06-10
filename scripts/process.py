import os
import tempfile

temp_dir = tempfile.gettempdir()

def is_locked() -> bool:
	return os.path.isfile(f"{temp_dir}/disrichie.lock")

def lockfile_pid() -> int:
	if not is_locked():
		print('No lockfile exists, cannot get locked process ID.')
		return 0
	
	lockfile = open(f"{temp_dir}/disrichie.lock", 'r')
	pid = lockfile.readline()
	lockfile.close()
	return int(pid)

def init_lockfile():
	lockfile = open(f"{temp_dir}/disrichie.lock", 'w')
	lockfile.write(str(os.getpid()))
	lockfile.close()

def destroy_lockfile():
	if not is_locked():
		print('Lockfile has already been deleted.')
		return
	
	try:
		os.remove(f"{temp_dir}/disrichie.lock")
	except FileNotFoundError:
		print('Cannot delete lockfile, maybe the lockfile was deleted unexpectedly?')
