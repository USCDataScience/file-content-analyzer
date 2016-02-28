import os

class HTFileReader:
  def __init__(self, filePath, offset):
    self.inputFile = open(filePath, 'r')
    self.offset = offset
    self.fileSize = os.path.getsize(filePath)

  def read(self, process):

    if self.fileSize < self.offset:
      bs = self.inputFile.read(self.fileSize)
      headBytes = bs
      tailBytes = bs
    else:
      self.inputFile.seek(0, 0)
      headBytes = self.inputFile.read(self.offset)
      self.inputFile.seek( self.fileSize - self.offset , 0)
      tailBytes = self.inputFile.read(self.offset)

    process(headBytes, tailBytes)

    self.stop()

  def stop(self):
    self.inputFile.close()
