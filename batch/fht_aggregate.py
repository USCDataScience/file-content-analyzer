from multiprocessing import Pool
import sys
import subprocess
import math
from os import listdir
from os.path import join

sys.path.insert(0, "..")
from fht.average import *
from fht.fht import *


# Path to the signature folder
PATH   = sys.argv[1]

# Path to the accumulated signatures
OUTPUT_PATH  = sys.argv[2]

OFFSET = int(sys.argv[3])

def fileLength(fname):
  p = subprocess.Popen(['wc', '-c', fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  result, err = p.communicate()
  if p.returncode != 0:
      raise IOError(err)
  return int(result.strip().split()[0]) / ( 2 * OFFSET )

def trainingLength(total):
  if total <= 5:
    return total
  else:
    return int( math.floor( total * 0.75 ) )

def arrayToString(arr):
  return ",".join(map(str, arr))

def matrixToString(m):
  return "\n".join(map(arrayToString, m))

# for each signature file
def processSignatures(file):
  print "-- STARTED -- {0}".format(file)

  initHead = [ [0 for x in range(256)] for x in range(OFFSET) ]
  initTrail = [ [0 for x in range(256)] for x in range(OFFSET) ]
  avg = FHTAverage((initHead, initTrail), 1)

  total = fileLength(join(PATH, "{0}-{1}".format(file, OFFSET)))
  train = trainingLength(total)

  f = open(join(PATH, "{0}-{1}".format(file, OFFSET)), 'r')

  for i in range(train):
    hBytes = f.read(OFFSET)
    tBytes = f.read(OFFSET)
    fht = FHTAnalyzer(OFFSET)
    fht.compute(hBytes, tBytes)
    avg = avg.accumulate(fht.signature())

  hSig,tSig = avg.fingerprint()

  op = open(join(OUTPUT_PATH, "{0}-{1}".format(file, OFFSET)), "w+")
  op.write(str(OFFSET))
  op.write("\n")
  op.write( matrixToString(hSig) )
  op.write("\n")
  op.write( matrixToString(tSig) )
  op.close()

  print "-- COMPLETED -- {0}".format(file)

TYPES = [
  "application-atom+xml",
  "application-dif+xml",
  "application-dita+xml; format=concept",
  "application-epub+zip",
  "application-fits",
  "application-gzip",
  "application-java-vm",
  "application-msword",
  "application-octet-stream",
  "application-pdf",
  "application-postscript",
  "application-rdf+xml",
  "application-rss+xml",
  "application-rtf",
  "application-vnd.google-earth.kml+xml",
  "application-vnd.ms-excel.sheet.4",
  "application-vnd.ms-htmlhelp",
  "application-vnd.rn-realmedia",
  "application-x-7z-compressed",
  "application-x-bibtex-text-file",
  "application-x-bittorrent",
  "application-x-bzip2",
  "application-x-compress",
  "application-x-debian-package",
  "application-x-elc",
  "application-x-executable",
  "application-x-font-ttf",
  "application-x-grib",
  "application-x-gtar",
  "application-x-hdf",
  "application-x-java-jnilib",
  "application-x-lha",
  "application-x-matroska",
  "application-x-msdownload",
  "application-x-msdownload; format=pe",
  "application-x-msdownload; format=pe32",
  "application-x-msmetafile",
  "application-x-rar-compressed",
  "application-x-rpm",
  "application-x-sh",
  "application-x-shockwave-flash",
  "application-x-sqlite3",
  "application-x-stuffit",
  "application-x-tar",
  "application-x-tex",
  "application-x-tika-msoffice",
  "application-x-tika-ooxml",
  "application-x-xz",
  "application-xhtml+xml",
  "application-xml",
  "application-xslt+xml",
  "application-zip",
  "application-zlib",
  "audio-basic",
  "audio-mp4",
  "audio-mpeg",
  "audio-x-aiff",
  "audio-x-flac",
  "audio-x-mpegurl",
  "audio-x-ms-wma",
  "audio-x-wav",
  "image-gif",
  "image-jpeg",
  "image-png",
  "image-svg+xml",
  "image-tiff",
  "image-vnd.adobe.photoshop",
  "image-vnd.dwg",
  "image-vnd.microsoft.icon",
  "image-x-bpg",
  "image-x-ms-bmp",
  "image-x-xcf",
  "message-rfc822",
  "message-x-emlx",
  "text-html",
  "text-plain",
  "text-troff",
  "text-x-csrc",
  "text-x-diff",
  "text-x-jsp",
  "text-x-matlab",
  "text-x-perl",
  "text-x-php",
  "text-x-python",
  "text-x-vcard",
  "video-mp4",
  "video-mpeg",
  "video-quicktime",
  "video-x-flv",
  "video-x-m4v",
  "video-x-ms-asf",
  "video-x-ms-wmv",
  "video-x-msvideo",
]

p = Pool(1)
p.map(processSignatures, TYPES)
