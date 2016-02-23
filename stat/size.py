from multiprocessing import Pool
from os import listdir, stat
from os.path import join, isdir, getsize

import sys

def listFolders(path):
  return filter(lambda f: isdir(join(path, f)), listdir(path))

PATH   = sys.argv[1]
OUTPUT = sys.argv[2]

def processFolder(path, tp, folder, sizeFile):
  print "-- STARTED -- {0}".format(join(path, tp, folder))
  for file in listdir(join(path, tp, folder)):
    sizeFile.write("{0},{1}\n".format(file, stat(join(path, tp, folder, file)).st_size))
  print "-- COMPLETED -- {0}".format(join(path, tp, folder))

def processType(tp):
  for f in listFolders(join(PATH, tp)):
    sizeFile = open(join(OUTPUT, tp), "a")
    processFolder(PATH, tp, f, sizeFile)
    sizeFile.close()

p = Pool()
p.map(processType, listFolders(PATH))
