from multiprocessing import Pool
from os.path import join

from download import *
import sys

FOLDERS = [
  "1", "107", "108", "118", "12", "137", "140", "16", "160", "170", "171", "188",
  "19", "198", "201", "202", "21", "213", "218", "250", "28", "42", "44", "51",
  "55", "57", "63", "73", "90", "92", "ae", "aero", "ag", "ai", "al", "am",
  "aq", "ar", "at", "au", "ax", "bb", "be", "bg", "biz", "br", "ca", "camp",
  "cat", "cc", "ch", "cl", "club", "cm", "cn", "co", "com", "coop", "cr", "cu",
  "cx", "cz", "de", "dj", "dk", "do", "ec", "edu", "ee", "eg", "enlace", "es",
  "et", "eu", "fi", "fj", "fm", "fr", "gd", "gl", "gov", "gr", "gs", "gy",
  "help", "hk", "hr", "hu", "id", "ie", "il", "im", "in", "info", "int", "io",
  "ir", "is", "it", "jobs", "jp", "ke", "kr", "ky", "kz", "la", "land", "li",
  "link", "lt", "lu", "lv", "ly", "ma", "md", "me", "media", "mil", "mn", "mo",
  "mobi", "mp", "ms", "museum", "mx", "my", "name", "ne", "net", "ng", "ninja",
  "nl", "no", "nr", "nu", "nz", "org", "ovh", "pe", "ph", "pk", "pl", "pr", "pro",
  "pt", "pw", "re", "ro", "rs", "ru", "sa", "sc", "se", "sg", "sh", "si", "sk",
  "sm", "st", "th", "tk", "tm", "to", "tr", "travel", "tt", "tv", "tw", "ua", "ug",
  "uk", "us", "uy", "ve", "vg", "vn", "vu", "ws", "za", "zm"
]


def load(folder):
  dfs_traversal(join(sys.argv[1], folder), sys.argv[2])
  print " ---- COMPLETED ---- {0}".format(folder)
  return

if __name__ == '__main__':
  p = Pool(5)
  p.map(load, FOLDERS)
