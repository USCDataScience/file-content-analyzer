from os import listdir, mkdir, rename
from os.path import isfile, join, isdir
from shutil import copyfile, rmtree, move

import sys
from file_count import *

import pdb

PATH = sys.argv[1]

def listFolders(path):
  return filter(lambda f: isdir(join(path, f)), listdir(path))

def initTypeDir(path):
  if not isdir(path):
    mkdir(path)
    mkdir(join(path, "1"))
    FileCountHandler(path).writeCount(0)

def processType(tp, sourcePath):
  print "-- STARTED -- {0}".format(sourcePath)
  destPath = join(PATH, tp)
  initTypeDir(destPath)

  # Update File count ( Sum of source and destination files )
  dFileCount = FileCountHandler(destPath)
  sFileCount = FileCountHandler(sourcePath)
  dFileCount.writeCount( dFileCount.readCount() + sFileCount.readCount() )

  dFolders = map(int, listFolders(destPath))  
  dFolderCount = max(dFolders)

  sFolders = map(int, listFolders(sourcePath))
  sFolderCount = max(sFolders)

  #Move last folder temporarily
  tmpFolder = join(destPath, "tmp")
  rename(join(destPath, str(dFolderCount)), tmpFolder)

  # All elements except the last
  for sFolder in sFolders[:-1]:
    fromFolder = join(sourcePath, str(sFolder))
    toFolder = join(destPath, str(sFolder + dFolderCount - 1))

    mkdir(toFolder)
    # MOVE FOLDER
    rename(fromFolder, toFolder)

  lastSourceFolder = join(sourcePath, str(sFolders[-1:][0]))
  x = len(listdir(lastSourceFolder))
  y = len(listdir(tmpFolder))

  # Count after partial merge
  partialCount = dFolderCount + sFolderCount - 2
  partialFolder = join(destPath, str(partialCount + 1))
  finalDestFolder = join(destPath, str(partialCount + 2))

  # Merge lastSourceFolder and tmpFolder
  rename(tmpFolder, partialFolder)

  if y < 100:
    difference = 100 - y
    for f in listdir(lastSourceFolder)[:difference]:
      rename(join(lastSourceFolder, f), join(partialFolder, f))

    if len(listdir(lastSourceFolder)) > 0:
      mkdir(finalDestFolder) 
      rename(lastSourceFolder, finalDestFolder)

  else:
    mkdir(finalDestFolder) 
    rename(lastSourceFolder, finalDestFolder)

  print "-- COMPLETED -- {0}".format(sourcePath)

def processDir(dPath):
  print "-- STARTED -- {0}".format(dPath)
  for tp in listdir(dPath):
    tPath = join(dPath, tp)
    processType(tp, tPath)
  rmtree(dPath)
  print "-- COMPLETED -- {0}".format(dPath)

for klass in listFolders(PATH):
  d = join(PATH, klass)
  processDir(d)