from os import listdir, mkdir
from os.path import isfile, join, isdir
from shutil import copyfile
from tika import detector
from shutil import move

import ntpath
import re
import sys
import time

def safeMakeDir(path):
  if not isdir(path):
    mkdir(path)

def writeFile(folder, fileName, tmpPath):
  fPath = join(folder, fileName)
  move(tmpPath, fPath)
  print "{0}".format(fPath)


def fetchFile(path, END_POINT):
  fileName = "{0}-{1}".format(ntpath.basename(path), time.time())

  # Download File
  tmpPath = join(END_POINT, fileName)
  copyfile(path, tmpPath)

  # Run Tika
  tp = detector.from_file(path).replace("/", "-")

  d = join(END_POINT, tp)

  safeMakeDir(d)

  writeFile(d, fileName, tmpPath)


def dfs_traversal(path, END_POINT):
  if isfile(path):
    fetchFile(path, END_POINT)
    return

  for f in listdir(path):
    dfs_traversal(join(path, f), END_POINT)

if __name__ == '__main__':
  MOUNT_POINT = sys.argv[1]
  END_POINT = sys.argv[2]

  dfs_traversal(MOUNT_POINT, END_POINT)
