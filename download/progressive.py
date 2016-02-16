from multiprocessing import Pool
from os.path import join

from download import *
import sys

from os import listdir

FOLDERS = listdir(sys.argv[1])

DONE_LIST = ["org", "com"]

def load(folder):
  print " ---- STARTED ---- {0}".format(folder)

  safeMakeDir(join(sys.argv[2], folder))
  dfs_traversal(join(sys.argv[1], folder), join(sys.argv[2], folder))

  print " ---- COMPLETED ---- {0}".format(folder)

  return

if __name__ == '__main__':
  p = Pool()
  left = filter(lambda f: f not in DONE_LIST, FOLDERS)
  p.map(load, left)
