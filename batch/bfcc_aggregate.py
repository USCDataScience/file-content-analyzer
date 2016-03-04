from multiprocessing import Pool
import sys
import subprocess
import math
from os import listdir
from os.path import join

sys.path.insert(0, "..")
from bfa.average import *
from bfa.cross import *

# Signatures
SIGNATUE_PATH = sys.argv[1]

# output signature path
OUTPUT_PATH  = sys.argv[2]

def fileLength(fname):
  p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  result, err = p.communicate()
  if p.returncode != 0:
    raise IOError(err)
  return int(result.strip().split()[0])

def trainingLength(total):
  if total <= 5:
    return total
  else:
    return int( math.floor( total * 0.75 ) )

def arrayToString(arr):
  return ",".join(map(str, arr))


# for each signature file
def processSignatures(file):
  print "-- STARTED -- {0}".format(file)

  sg = open(join(SIGNATUE_PATH, file), "r")
  s = map(float, sg.readline().split(","))

  c = BFCrossCorrelator(s)
  c.correlate()

  op = open(join(OUTPUT_PATH, file), "w+")
  op.write( str(c) )
  op.close()

  print "-- COMPLETED -- {0}".format(file)

p = Pool(20)
p.map(processSignatures, listdir(SIGNATUE_PATH))
