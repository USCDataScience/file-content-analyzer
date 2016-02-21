from os import listdir, mkdir, rename
from os.path import join, isdir
import sys

def listFolders(path):
  return filter(lambda f: isdir(join(path, f)), listdir(path))

def safeMkdir(path):
  if not isdir(path):
    mkdir(path)

PATH = sys.argv[1]

def mergeParts(path):
  for partPath in listFolders(path):
    for tp in listFolders(join(path, partPath)):
      print "-- STARTED -- {0}".format(join(path, partPath, tp))
      # Create type path
      safeMkdir(join(path, tp))
      for fold in listFolders(join(path, partPath, tp)):
        rename(join(path, partPath, tp, fold), join(path, tp, fold))
      print "-- COMPLETED -- {0}".format(join(path, partPath, tp))

mergeParts(PATH)
