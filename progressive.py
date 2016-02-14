from multiprocessing import Pool
from os.path import join

from download import *
import sys

from os import listdir

FOLDERS = listdir(sys.argv[1])


def load(folder):
  print " ---- STARTED ---- {0}".format(folder)
  dfs_traversal(join(sys.argv[1], folder), sys.argv[2])
  print " ---- COMPLETED ---- {0}".format(folder)

  with open("done.log", "a") as f:
    f.write("{0}\n".format(folder))

  return

if __name__ == '__main__':
  p = Pool(20)
  p.map(load, FOLDERS)
