#!/usr/bin/env python3

import shutil
import urllib.request
import os

homedir = os.environ['HOME']
homedir = homedir + "/"
downloaddir = homedir + "Downloads"
dlconfigdir = homedir + ".config/pydownloader/dlconfig"
moveconfigdir = homedir + ".config/pydownloader/moveconfig"
dlconfig = dlconfigdir + "/dlconfig"
moveconfig = moveconfigdir + "/moveconfig"

print("Checking if Download Config Directory exists...")
if not os.path.exists(dlconfigdir):
	print("Download Config Directory does not exist, creating it now...")
	os.makedirs(dlconfigdir)
print("Checking if Move Config Directory exists...")	
if not os.path.exists(moveconfigdir):
	print("Move Config Directory does not exist, creating it now...")
	os.makedirs(moveconfigdir)

os.chdir(dlconfigdir)

print("Checking if Download config file exists...")
try:
	config_file = open(dlconfig)
except IOError:
	print("Download config file does not exist, creating it now...")
	open(dlconfig, 'a').close()


os.chdir(moveconfigdir)

print("Checking if Move config file exists...")
try:
	move_config_file = open(moveconfig)
except IOError:
	print("Move config file does not exist, creating it now...")
	open(dlconfig, 'a').close()

if (os.stat("moveconfig").st_size == 0):
	print("moveconfig is empty, please add to it to continue.")
	sys.exit(0)

os.chdir(dlconfigdir)

if (os.stat("dlconfig").st_size == 0):
	print("dlconfig is empty, please add to it to continue.")
	sys.exit(0)

print("Changing directory to $HOME/Downloads.")
os.chdir(downloaddir)

print("\n")
print("Opening Download config file for reading.")
for dlconfig in os.listdir(dlconfigdir):
	with open(os.path.join(dlconfigdir, dlconfig), encoding='utf-8') as a_file:
		for a_line in a_file:
			line = a_line[:1]
			if (line == "*"):
				url = a_line[1::]
				url = url.rstrip('\n')
			if (line == "#"):
				file_name = a_line[1::]
				file_name = file_name.rstrip('\n')
	print("Downloading files now...")
	with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
		data = response.read()
		out_file.write(data)

print("Files are finished downloading.  Now moving files to appropriate directories...")
for moveconfig in os.listdir(moveconfigdir):
	with open(os.path.join(moveconfigdir, moveconfig), encoding='utf-8') as a_file:
		for a_line in a_file:
			line = a_line[:1]
			if (line == "*"):
				extractdir = a_line[1::]
				extractdir = extractdir.rstrip('\n')
				workingdir = homedir + extractdir
			if (line == "#"):
				file_extension = a_line[1::]
				file_extension = file_extension.rstrip('\n')
				for root, dirs, files in os.walk(downloaddir):
					for f_name in files:
						if f_name.endswith(file_extension):
							shutil.move(f_name, workingdir)
