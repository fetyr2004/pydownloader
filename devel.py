#!/usr/bin/env python3

import shutil
import urllib.request
import os
import sys
from urllib.request import urlretrieve

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

homedir = os.environ['HOME']
homedir = homedir + "/"
downloaddir = homedir + "Downloads"
dlconfigdir = homedir + ".config/pydownloader/dlconfig"
moveconfigdir = homedir + ".config/pydownloader/moveconfig"
dlconfig = dlconfigdir + "/dlconfig"
moveconfig = moveconfigdir + "/moveconfig"

print("Checking if download config directory exists...")
if not os.path.exists(dlconfigdir):
    print("Download config directory does not exist, creating it now...")
    os.makedirs(dlconfigdir)
print("Checking if move config directory exists...")
if not os.path.exists(moveconfigdir):
    print("Move config directory does not exist, creating it now...")
    os.makedirs(moveconfigdir)

os.chdir(dlconfigdir)

print("Checking if download config file exists...")
try:
    config_file = open(dlconfig)
except IOError:
    print("Download config file does not exist, creating it now...")
    open(dlconfig, 'a').close()

os.chdir(moveconfigdir)

print("Checking if move config file exists...")
try:
    move_config_file = open(moveconfig)
except IOError:
    print("Move config file does not exist, creating it now...")
    open(moveconfig, 'a').close()

if (os.stat("moveconfig").st_size == 0):
        print("moveconfig is empty, please add to it to continue.")
        sys.exit(0)

os.chdir(dlconfigdir)

if (os.stat("dlconfig").st_size == 0):
    print("dlconfig is empty, please add to it to continue.")
    sys.exit(0)

print("Changing directory to $HOME/Downloads")
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
    print("Downloading files.now...")
    urlretrieve(url, file_name, reporthook)
