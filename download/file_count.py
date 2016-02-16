from os.path import join

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