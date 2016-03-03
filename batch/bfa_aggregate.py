from multiprocessing import Pool
import sys
import subprocess
import math
from os import listdir
from os.path import join

sys.path.insert(0, "..")
from bfa.average import *

# Path to the signature folder
PATH   = sys.argv[1]

# Path to the accumulated signatures
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

  initFreq = map(lambda x: float(0), range(256))
  avg = BFAverage(initFreq, 1)

  total = fileLength(join(PATH, file))
  train = trainingLength(total)

  f = open(join(PATH,file), 'r')

  for l in range(train):
    line = f.readline()
    try:
      sig = map(float, line.split(",")[2:])
      avg = avg.accumulate(sig)
    except Exception as e:
      print e

  op = open(join(OUTPUT_PATH, file), "w+")
  op.write(arrayToString(avg.signature()))
  op.close()

  print "-- COMPLETED -- {0}".format(file)

p = Pool(20)
p.map(processSignatures, listdir(PATH))
