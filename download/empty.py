from multiprocessing import Pool
from os import listdir, stat, rename, mkdir, rmdir
from os.path import join, isdir, getsize

import sys

def listFolders(path):
  return filter(lambda f: isdir(join(path, f)), listdir(path))

def safeMkdir(path):
  if not isdir(path):
    mkdir(path)

PATH   = sys.argv[1]

def processFolder(folder):
  print "-- STARTED -- {0}".format(join(PATH, folder))
  for file in listdir(join(PATH, folder)):
    if stat(join(PATH, folder, file)).st_size == 0:
      safeMkdir(join(PATH, "EMPTY", folder))
      rename(join(PATH, folder, file), join(PATH, "EMPTY", folder, file))
  print "-- COMPLETED -- {0}".format(join(PATH, folder))

safeMkdir(join(PATH, "EMPTY"))
folders = filter(lambda x: x not in ["EMPTY"], listFolders(PATH))

p = Pool()
p.map(processFolder, folders)

#DELETE EMPTY FOLDERS
print "---- Deleting EMPTY folders ----"
for f in folders:
  if len(listdir(join(PATH, f))) == 0:
    rmdir(join(PATH, f))
print "---- Deleted EMPTY folders ----"
