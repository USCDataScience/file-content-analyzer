import sys
from os import mkdir
from os.path import join, isdir
import time

from rw.reader import *
from bfa.bfa import *
from bfa.compare import *
from bfa.cross import *

from rw.ht_reader import *
from fht.fht import *

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
  fileName = "computed"
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
  fileName = "computed"
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
  fileName = "computed"
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


def runFHT():
  SFILE_PATH = sys.argv[2]
  OFFSET = int(sys.argv[3])

  safeMkdir(join("output", "fht"))
  fileName = "computed"
  OP_PATH = join("output", "fht", str(fileName))

  r = HTFileReader(SFILE_PATH, OFFSET)
  fht = FHTAnalyzer(OFFSET)
  r.read(fht.compute)

  f = open(OP_PATH, "w+")
  (hSig, fSig) = fht.signature()
  f.write(str(OFFSET))
  f.write("\n")
  f.write( matrixToString(hSig) )
  f.write("\n")
  f.write( matrixToString(fSig) )
  f.close()

  print " ------ FHT Matrix Computed ------ "
  print " The HTML matrix has been saved in {0} ".format(OP_PATH)
  print " RUN: cp ./output/fht/* /WEB_APP/data/computed/fht "
  print " You can view the visualization at {0}#/visualize/fht/{1}/{2}".format(VISUALIZATION_APP, OFFSET, fileName)
  print " ------ VISUALIZATION READY ------ "

# CREATE OUTPUT PATH
safeMkdir("output")

if TYPE == "bfa":
  runBFA()
elif TYPE == "bfc":
  runBFC()
elif TYPE == "bfcc":
  runBFCC()
elif TYPE == "fht":
  runFHT()


print " Ensure that you have the visualization engine running as a Grunt JS app ( or ) "
print " served as a HTML app via a web server like NGINX "
print " Example-Path to the app: {0} ".format(VISUALIZATION_APP)
