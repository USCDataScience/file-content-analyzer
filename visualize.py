import sys
from os import mkdir
from os.path import join, isdir
import time

from rw.reader import *
from bfa.bfa import *
from bfa.compare import *
from bfcc.bfcc import *

# TYPE of operation
TYPE = sys.argv[1]

VISUALIZATION_APP = "http://localhost:9000"

def safeMkdir(path):
  if not isdir(path):
    mkdir(path)

def arrayToString(arr):
  return ",".join(map(str, arr))

def matrixToString(m):
  return "\n".join(map(arrayToString, m))

def runBFA():
  SFILE_PATH = sys.argv[2]

  safeMkdir(join("output", "bfa"))
  fileName = time.time()
  OP_PATH = join("output", "bfa", str(fileName))

  r = FileReader(SFILE_PATH)
  a = BFAnalyzer()
  r.read(a.compute)

  f = open(OP_PATH, "w+")
  f.write( arrayToString(a.smoothen()) )
  f.close()

  print " ------ BFA Signature Computed ------ "
  print " The signature has been saved in {0} ".format(OP_PATH)
  print " RUN: cp ./output/bfa/* /WEB_APP/data/computed/bfa "
  print " You can view the visualization at {0}#/visualize/bfa/{1}".format(VISUALIZATION_APP, fileName)
  print " ------ VISUALIZATION READY ------ "

def runBFC():
  SFILE_PATH = sys.argv[2]
  CFILE_PATH = sys.argv[3]

  safeMkdir(join("output", "bfc"))
  fileName = time.time()
  OP_PATH = join("output", "bfc", str(fileName))

  r1 = FileReader(SFILE_PATH)
  a1 = BFAnalyzer()
  r1.read(a1.compute)

  r2 = FileReader(CFILE_PATH)
  a2 = BFAnalyzer()
  r2.read(a2.compute)

  baseSignature = a1.smoothen()
  cmpSignature = a2.smoothen()
  c = ByteFrequencyCorrelator(baseSignature)

  f = open(OP_PATH, "w+")
  f.write( arrayToString(baseSignature) )
  f.write("\n")
  f.write( arrayToString(cmpSignature) )
  f.write("\n")
  f.write( arrayToString(c.correlate(cmpSignature)) )
  f.close()

  print " ------ BF Correlation Computed ------ "
  print " The correlation has been saved in {0} ".format(OP_PATH)
  print " RUN: cp ./output/bfc/* /WEB_APP/data/computed/bfc "
  print " You can view the visualization at {0}#/visualize/bfc/{1}".format(VISUALIZATION_APP, fileName)
  print " ------ VISUALIZATION READY ------ "

def runBFCC():
  SFILE_PATH = sys.argv[2]

  safeMkdir(join("output", "bfcc"))
  fileName = time.time()
  OP_PATH = join("output", "bfcc", str(fileName))

  r = FileReader(SFILE_PATH)
  a = BFAnalyzer()
  r.read(a.compute)

  signature = a.smoothen()
  c = BFCrossCorrelator(signature)

  f = open(OP_PATH, "w+")
  f.write( matrixToString(c.correlate()) )
  f.close()

  print " ------ BF Cross Correlation Computed ------ "
  print " The cross-correlation matrix has been saved in {0} ".format(OP_PATH)
  print " RUN: cp ./output/bfcc/* /WEB_APP/data/computed/bfcc "
  print " You can view the visualization at {0}#/visualize/bfcc/{1}".format(VISUALIZATION_APP, fileName)
  print " ------ VISUALIZATION READY ------ "

# CREATE OUTPUT PATH
safeMkdir("output")

if TYPE == "bfa":
  runBFA()
elif TYPE == "bfc":
  runBFC()
elif TYPE == "bfcc":
  runBFCC()


print " Ensure that you have the visualization engine running as a Grunt JS app ( or ) "
print " served as a HTML app via a web server like NGINX "
print " Example-Path to the app: {0} ".format(VISUALIZATION_APP)
