from multiprocessing import Pool
from os import listdir
from os.path import join, isdir

import sys

def listFolders(path):
  return filter(lambda f: isdir(join(path, f)), listdir(path))

PATH   = sys.argv[1]
OUTPUT = sys.argv[2]

def processFolder(path, tp, folder, sizeFile):
  print "-- STARTED -- {0}".format(join(path, tp, folder))
  for file in listdir(join(path, tp, folder)):
    sizeFile.write("{0}\n".format(os.path.getsize(join(path, tp, folder, file))))
  print "-- COMPLETED -- {0}".format(join(path, tp, folder))

def computeSizes(path):
  for tp in listFolders(path):
    sizeFile = open(join(OUTPUT, tp), "a")
    p = Pool(20)
    p.map(lambda f: processFolder(path, tp, f, sizeFile), listFolders(join(path, tp)))
    sizeFile.close()

computeSizes(PATH)
