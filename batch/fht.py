from multiprocessing import Pool
from os import listdir, stat
from os.path import join, isdir

import sys

sys.path.insert(0, "..")

from rw.ht_reader import *

def listFolders(path):
  return filter(lambda f: isdir(join(path, f)), listdir(path))

# Path to the type folder (ie) /application-octetstream
PATH   = sys.argv[1]

# Path where the signatures are accumulated
SIGNATURE_PATH = sys.argv[2]

THREADS = int(sys.argv[3])

def writeBytesToFile(path):
  def writer(hBytes, tBytes):
    f = open(path, "a")
    f.write(hBytes)
    f.write(tBytes)
    f.write("\n")
    f.close()
  return writer

def processFolder(folder):
  print "-- STARTED -- {0}".format(join(PATH, folder))

  for file in listdir(join(PATH, folder)):
    filePath = join(PATH, folder, file)
    HTFileReader(filePath, 8).read(writeBytesToFile("{0}-{1}".format(SIGNATURE_PATH, 8)))
    HTFileReader(filePath, 16).read(writeBytesToFile("{0}-{1}".format(SIGNATURE_PATH, 16)))
    HTFileReader(filePath, 32).read(writeBytesToFile("{0}-{1}".format(SIGNATURE_PATH, 32)))

  print "-- COMPLETED -- {0}".format(join(PATH, folder))

for f in listFolders(PATH):
	processFolder(f)
#p = Pool(THREADS)
#p.map(processFolder, listFolders(PATH))







