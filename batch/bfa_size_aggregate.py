from multiprocessing import Pool
import sys
import subprocess
import math
from os import listdir
from os.path import join

sys.path.insert(0, "..")
from bfa.average import *

SIZE_CLUSTERS = {
  'application-atom+xml': [ 10743,28827,51944,107740,207874 ],
  'application-dif+xml': [ 2956,3688,5071,7576,15906 ],
  'application-dita+xml; format=concept': [ 1833,3692,9737,35417,64896 ],
  'application-epub+zip': [ 58131,59481,60945,63888,65536 ],
  'application-gzip': [ 16227,47116,183617,1006987,17304885 ],
  'application-octet-stream': [ 47104,262656,1600000,12955944,33554432 ],
  'application-pdf': [ 564977,1933142,8400506,26387340,80494469 ],
  'application-postscript': [ 34332,53807,244668,614210,1081074 ],
  'application-rdf+xml': [ 4786,14235,28967,50848,105225 ],
  'application-rss+xml': [ 9425,26320,51168,816838,2507098 ],
  'application-rtf': [ 20069,44316,65536,185575,1253184 ],
  'application-vnd.google-earth.kml+xml': [ 14986,42830,118279,256638,2000000 ],
  'application-vnd.rn-realmedia': [ 62006,63449,63455,65536,125303 ],
  'application-x-bibtex-text-file': [ 932,2739,5099,11602,25231 ],
  'application-x-bzip2': [ 61038,62498,63388,63956,65536 ],
  'application-x-compress': [ 327865,3060297,4527635,5677012,8171903 ],
  'application-x-elc': [ 4237,11328,17849,33381,260018 ],
  'application-x-executable': [ 61051,63971,65536,230464,4128088 ],
  'application-x-gtar': [ 20480,40960,62729,64907,65536 ],
  'application-x-hdf': [ 40515,65536,5176650,16631632,33554432 ],
  'application-x-matroska': [ 1286236,3462682,8471145,21987116,33554370 ],
  'application-x-msdownload': [ 18384,59585,64116,65536,2000000 ],
  'application-x-msdownload; format=pe32': [ 63965,65422,65536,2000000,6126781 ],
  'application-x-sh': [ 16981,37433,56053,139577,861653 ],
  'application-x-shockwave-flash': [ 23344,50233,177215,610324,2000000 ],
  'application-x-tar': [ 10240,30720,61048,63969,65536 ],
  'application-x-tex': [ 3439,9141,20932,35464,65536 ],
  'application-x-tika-ooxml': [ 45438,346833,1007144,3675469,11443216 ],
  'application-xhtml+xml': [ 16327,27914,39514,56928,10252681 ],
  'application-xml': [ 6990,16814,48293,513116,1223934 ],
  'application-xslt+xml': [ 1202,4641,5229,12478,31658 ],
  'application-zip': [ 56448,1296759,7933609,36104887,93705162 ],
  'application-zlib': [ 59590,63972,65536,2655360,2655360 ],
  'audio-basic': [ 19832,34154,52700,65536,119576 ],
  'audio-mp4': [ 34647,48281,55973,61791,64688 ],
  'audio-mpeg': [ 44046,65536,348672,4292737,17457930 ],
  'audio-x-aiff': [ 63467,64915,65536,33548950,33551096 ],
  'audio-x-ms-wma': [ 63460,64903,64908,65536,2000000 ],
  'audio-x-wav': [ 24828,48958,62204,65536,170038 ],
  'image-gif': [ 11085,42923,201746,835665,2655360 ],
  'image-jpeg': [ 40989,451466,1504728,4180030,15625829 ],
  'image-png': [ 50642,551421,3084833,11421673,33552478 ],
  'image-svg+xml': [ 2852,8480,20374,37416,98304 ],
  'image-tiff': [ 1093480,4839100,10444060,21614653,84352072 ],
  'image-vnd.microsoft.icon': [ 2330,4710,13942,31030,65536 ],
  'image-x-bpg': [ 548,6356,11860,13401,49181 ],
  'image-x-ms-bmp': [ 2102,12342,24906,65536,720054 ],
  'message-rfc822': [ 901,4833,14667,48675,151901 ],
  'text-html': [ 18788,48818,88289,190484,8695887 ],
  'text-plain': [ 15553,46773,140960,1035276,43492762 ],
  'text-x-matlab': [ 3588,13055,29926,47640,66615 ],
  'text-x-perl': [ 1141,2176,3920,8380,13979 ],
  'text-x-php': [ 492,4286,14291,29465,63508 ],
  'text-x-vcard': [ 301,335,349,359,6726 ],
  'video-mp4': [ 62320,64168,65536,15960988,33554309 ],
  'video-mpeg': [ 74534,2987843,9514306,22030370,33554230 ],
  'video-quicktime': [ 65536,1821980,8286365,22672279,33554416 ],
  'video-x-flv': [ 58157,63997,65176,65536,2000000 ],
  'video-x-m4v': [ 62004,65536,4220426,9563827,33554416 ],
  'video-x-ms-asf': [ 60537,62012,63460,64909,65536 ],
  'video-x-ms-wmv': [ 63461,65536,4243076,18517824,33554432 ],
  'video-x-msvideo': [ 63970,65536,631808,2299904,33554066 ],
}

import pdb

# Path to the signature folder
PATH   = sys.argv[1]

# Path to the accumulated signatures
OUTPUT_PATH  = sys.argv[2]

def arrayToString(arr):
  return ",".join(map(str, arr))

def bucketFromSize(file,size):
  buckets = SIZE_CLUSTERS[file]

  if size <= buckets[0]:
    return 0
  elif size <= buckets[1]:
    return 1
  elif size <= buckets[2]:
    return 2
  elif size <= buckets[3]:
    return 3
  elif size <= buckets[4]:
    return 4
  else:
    return 5

# for each signature file
def processSignatures(file):
  if file not in SIZE_CLUSTERS:
    return

  try:
    print "-- STARTED -- {0}".format(file)

    avg = [ ]

    for i in range(5):
      avg = avg + [ BFAverage(map(lambda x: float(0), range(256)), 1) ]

    f = open(join(PATH,file), 'r')

    for line in f:
      parts = line.split(",")
      size = float(parts[1])
      sig = map(float, parts[2:])
      bucket = bucketFromSize(file, size)
      avg[bucket] = avg[bucket].accumulate(sig)


    for i in range(5):
      op = open(join(OUTPUT_PATH, "{0}-{1}".format(file, i+1)), "w+")
      op.write(arrayToString(avg[i].signature()))
      op.close()

    print "-- COMPLETED -- {0}".format(file)

  except Exception as e:
    print "-- ERROR -- {0}".format(file)
    print e

p = Pool(20)
p.map(processSignatures, listdir(PATH))

