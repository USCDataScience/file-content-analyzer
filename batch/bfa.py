from multiprocessing import Pool
from os import listdir, stat
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

def writeSignatureToFile(signature, filePath):
  f = open(SIGNATURE_PATH, "a")
  sigString = ",".join(map(str, signature))
  fileSize = stat(filePath).st_size
  f.write("{0},{1},{2}\n".format(filePath, fileSize, sigString))
  f.close()

def processFolder(folder):
  print "-- STARTED -- {0}".format(join(PATH, folder))

  for file in listdir(join(PATH, folder)):
    filePath = join(PATH, folder, file)
    reader = FileReader(filePath)
    analyzer = BFAnalyzer()
    reader.read(analyzer.compute)
    writeSignatureToFile(analyzer.smoothen(), filePath)

  print "-- COMPLETED -- {0}".format(join(PATH, folder))

p = Pool(THREADS)
p.map(processFolder, listFolders(PATH))
