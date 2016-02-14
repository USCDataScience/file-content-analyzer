from os import listdir, mkdir
from os.path import isfile, join, isdir
from shutil import copyfile
from tika import detector
from shutil import move

import ntpath
import re
import sys
import time

import pdb


class FileCountHandler:
  def __init__(self, path):
    self.file = join(path,"count")

  def readCount(self):
    return int(tuple(open(self.file, "r"))[0])

  def writeCount(self, count):
    f = open(self.file, "w+")
    return f.write(str(count))

  def incrementCount(self):
    self.writeCount(self.readCount() + 1)

def safeMakeDir(path):
  if not isdir(path):
    mkdir(path)

def writeFile(folder, fileName, tmpPath):
  countH = FileCountHandler(folder)
  subFolder = countH.readCount() / 100
  safeMakeDir(join(folder, str(subFolder)))
  fPath = join(folder, str(subFolder), fileName)
  move(tmpPath, fPath)
  countH.incrementCount()
  print "{0}".format(fPath)


def fetchFile(path, END_POINT):
  fileName = "{0}-{1}".format(ntpath.basename(path), time.time())

  # Download File
  tmpPath = join(END_POINT, fileName)
  copyfile(path, tmpPath)

  # Run Tika
  tp = detector.from_file(path).replace("/", "-")

  d = join(END_POINT, tp)

  if not isdir(d):
    safeMakeDir(d)
    FileCountHandler(d).writeCount(0)

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
