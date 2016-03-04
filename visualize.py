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
from fht.compare import *
from fht.average import *

# TYPE of operation
TYPE = sys.argv[1]

VISUALIZATION_APP = "http://localhost:9000"

def safeMkdir(path):
  if not isdir(path):
    mkdir(path)

def runBFA():
  SFILE_PATH = sys.argv[2]

  safeMkdir(join("output", "bfa"))
  fileName = "computed"
  OP_PATH = join("output", "bfa", str(fileName))

  r = FileReader(SFILE_PATH)
  a = BFAnalyzer()
  r.read(a.compute)
  a.smoothen()

  f = open(OP_PATH, "w+")
  f.write( str(a) )
  f.close()

  print " ------ BFA Signature Computed ------ "
  print " The signature has been saved in {0} ".format(OP_PATH)
  print " RUN: cp ./output/bfa/{0} WEBAPP_PATH/data/computed/bfa/".format(fileName)
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
  c.correlate(cmpSignature)

  f = open(OP_PATH, "w+")
  f.write( str(c) )
  f.close()

  print " ------ BF Correlation Computed ------ "
  print " The correlation has been saved in {0} ".format(OP_PATH)
  print " RUN: cp ./output/bfc/{0} WEBAPP_PATH/data/computed/bfc/".format(fileName)
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
  c.correlate()

  f = open(OP_PATH, "w+")
  f.write( str(c) )
  f.close()

  print " ------ BF Cross Correlation Computed ------ "
  print " The cross-correlation matrix has been saved in {0} ".format(OP_PATH)
  print " RUN: cp ./output/bfcc/{0} WEBAPP_PATH/data/computed/bfcc/".format(fileName)
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
  f.write( str(fht) )
  f.close()

  print " ------ FHT Matrix Computed ------ "
  print " The FHT matrix has been saved in {0} ".format(OP_PATH)
  print " RUN: cp ./output/fht/{0} WEBAPP_PATH/data/computed/fht/".format(fileName)
  print " You can view the visualization at {0}#/visualize/fht/{1}/{2}".format(VISUALIZATION_APP, OFFSET, fileName)
  print " ------ VISUALIZATION READY ------ "

def runFHTC():
  SFILE_PATH = sys.argv[2]
  CFILE_PATH = sys.argv[3]

  OFFSET = int(sys.argv[4])

  safeMkdir(join("output", "fht"))
  fileName = "correlation"
  OP_PATH = join("output", "fht", str(fileName))

  r1 = HTFileReader(SFILE_PATH, OFFSET)
  fht1 = FHTAnalyzer(OFFSET)
  r1.read(fht1.compute)

  r2 = HTFileReader(CFILE_PATH, OFFSET)
  fht2 = FHTAnalyzer(OFFSET)
  r2.read(fht2.compute)

  cm = CompareFHT(fht1.signature(), fht2.signature())
  cm.correlate()

  avg = FHTAverage(fht1.signature(), 1)
  avg = avg.accumulate(fht2.signature())

  f = open(OP_PATH, "w+")
  f.write( str(avg) )
  f.close()

  print " ------ FHT Correlation Computed ------ "
  print " The FHT matrix has been saved in {0} ".format(OP_PATH)
  print " THE Assurance Level for the 2 files is : {0}".format(cm.assuranceLevel())
  print " RUN: cp ./output/fht/{0} WEBAPP_PATH/data/computed/fht/".format(fileName)
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
elif TYPE == "fhtc":
  runFHTC()


print " Ensure that you have the visualization engine running as a Grunt JS app ( or ) "
print " served as a HTML app via a web server like NGINX "
print " Example-Path to the app: {0} ".format(VISUALIZATION_APP)
