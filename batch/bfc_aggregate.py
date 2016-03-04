from multiprocessing import Pool
import sys
import subprocess
import math
from os import listdir
from os.path import join

sys.path.insert(0, "..")
from bfa.average import *
from bfa.compare import *

# Batch signature
PATH          = sys.argv[1]

# Signatures
SIGNATURE_PATH = sys.argv[2]

# output signature path
OUTPUT_PATH  = sys.argv[3]

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

  initFreq = map(lambda x: float(0), range(256))
  avg = BFAverage(initFreq, 1)

  total = fileLength(join(PATH, file))
  train = trainingLength(total)

  trainRange = range(train, total) if train < total else range(total)

  f = open(join(PATH,file), 'r')

  for l in range(train, total):
    line = f.readline()
    try:
      sig = map(float, line.split(",")[2:])
      avg = avg.accumulate(sig)
    except Exception as e:
      print e

  s1 = avg.signature()

  sg = open(join(SIGNATURE_PATH, file), "r")
  s2 = map(float, sg.readline().split(","))

  c = ByteFrequencyCorrelator(s1)
  c.correlate(s2)

  op = open(join(OUTPUT_PATH, file), "w+")
  op.write( str(c) )
  op.close()

  print "-- COMPLETED -- {0}".format(file)

p = Pool(20)
p.map(processSignatures, listdir(PATH))
