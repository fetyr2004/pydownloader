#!/usr/bin/env python3

import shutil
import urllib.request
import os

#Specify Directories for working
homedir = os.environ['HOME']
homedir = homedir + "/"
downloaddir = homedir + "Downloads"
dlconfigdir = homedir + ".config/pydownloader/dlconfig"
moveconfigdir = homedir + ".config/pydownloader/moveconfig"

#Test to see if directories exist for config files, and if not create them and the files
if not os.path.exists(dlconfigdir):
	os.makedirs(dlconfigdir)
if not os.path.exists(moveconfigdir):
	os.makedirs(moveconfigdir)

os.chdir(dlconfigdir)

try:
	config_file = open(dlconfig)
except IOError:
	os.touch(dlconfig)

os.chdir(moveconfigdir)

try:
	move_config_file = open(moveconfig)
except IOError:
	os.touch(moveconfig)

#Change to /home/$USER/Downloads Directory to prepare for downloading
os.chdir(downloaddir)

#Open config file with download links and file names
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
#Download url's and save them with the specified file_name
	with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
		data = response.read()
		out_file.write(data)

#Open move config file and look for file extensions and directories
for moveconfig in os.listdir(moveconfigdir):
	with open(os.path.join(moveconfigdir, moveconfig), encoding='utf-8') as a_file:
		for a_line in a_file:
			line = a_line[:1]
			if (line == "*"):
				extractdir = a_line[1::]
				extractdir = extractdir.rstip('\n')
				workingdir = homedir + extractdir
			if (line == "#"):
				file_extension = a_line[1::]
				file_extenions = file_extension.rstrip('\n')
				for root, dirs, files in os.walk(downloaddir):
					for f_name in files:
						if f_name.endswith(file_extension):
							shutil.move(f_name, workingdir)
