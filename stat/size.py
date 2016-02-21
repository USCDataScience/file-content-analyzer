from multiprocessing import Pool
from os import listdir
from os.path import join, isdir, getsize

import sys

def listFolders(path):
  return filter(lambda f: isdir(join(path, f)), listdir(path))

PATH   = sys.argv[1]
OUTPUT = sys.argv[2]

def processFolder(d):
  (path, tp, folder) = d
  sizeFile = open(join(OUTPUT, tp), "a")
  print "-- STARTED -- {0}".format(join(path, tp, folder))
  for file in listdir(join(path, tp, folder)):
    sizeFile.write("{0}\n".format(getsize(join(path, tp, folder, file))))
  sizeFile.close()
  print "-- COMPLETED -- {0}".format(join(path, tp, folder))

def processType(path, tp):
  p = Pool(20)
  d = map(lambda f: (path, tp, f),listFolders(join(path, tp)))
  p.map(processFolder, d)

for tp in listFolders(PATH):
  processType(PATH, tp)
