from os import listdir, mkdir
from os.path import isfile, join, isdir
from shutil import copyfile

from tika import detector

import ntpath
import re

import sys


def fetchFile(path, END_POINT):
  tp = detector.from_file(path).replace("/", "-")
  fileName = ntpath.basename(path)

  if not isdir(join(END_POINT, tp)):
    mkdir(join(END_POINT, tp))

  copyfile(path, join(END_POINT, tp, fileName))
  print "{0} {1}".format(tp, fileName)


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
