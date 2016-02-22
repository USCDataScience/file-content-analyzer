from multiprocessing import Pool
from os import listdir
from os.path import join, isdir

import sys

sys.path.insert(0, "..")

from bfa.bfa   import *
from rw.reader import *

def listFolders(path):
  return filter(lambda f: isdir(join(path, f)), listdir(path))

# Path to the type folder (ie) /application-octetstream
PATH   = sys.argv[1]

# Path where the signatures are accumulated
SIGNATURE_PATH = sys.argv[2]

THREADS = int(sys.argv[3]) if len(sys.argv) > 3 else 20

def writeSignature(signature):
  f = open(SIGNATURE_PATH, "a")
  sigString = ",".join(map(str, signature))
  f.write("{0}\n".format(sigString))
  f.close()

def processFolder(folder):
  print "-- STARTED -- {0}".format(join(PATH, folder))

  for file in listdir(join(PATH, folder)):
    reader = FileReader(join(PATH, folder, file))
    analyzer = BFAnalyzer()
    reader.read(analyzer.compute)
    writeSignature(analyzer.smoothen())

  print "-- COMPLETED -- {0}".format(join(PATH, folder))

p = Pool(THREADS)
p.map(processFolder, listFolders(PATH))
