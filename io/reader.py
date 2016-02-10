from functools import partial
class FileReader:
  def __init__(self, filePath):
    self.inputFile = open(filePath, 'r')

  def read(self, process):
    for byte in iter(partial(self.inputFile.read, 1), ''):
      process( byte )

    self.stop()

  def stop(self):
    self.inputFile.close()
