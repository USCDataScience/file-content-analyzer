import sys
from os import listdir, mkdir
from os.path import isfile, join, isdir, getsize


path = sys.argv[1]

directories = listdir(path)
total = len(directories)
withData = 0

for f in directories:
  size = getsize(join(path, f))
  if size != 0:
    print join(path, f), size
    withData = withData + 1
  else:
    sys.stdout.write('.')


print "TOTAL NUMBER OF FILES {0}".format(total)
print "TOTAL NUMBER OF FILES WITH SOME DATA {0}".format(withData)

