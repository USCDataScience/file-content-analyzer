import math
import struct

class FHTAnalyzer:
  def __init__(self, offset):
    self.offset = offset
    self._signature = None

  def __handleSmallFiles(self, hBytes, tBytes):
    headSignature = [ [0 for x in range(256)] for x in range(self.offset) ]
    tailSignature = [ [0 for x in range(256)] for x in range(self.offset) ]

    for i in range(0, len(hBytes)):
      hVal = struct.unpack('B', hBytes[i])[0]
      headSignature[i][hVal] = 1

    for i in range(len(hBytes), self.offset):
      headSignature[i] = map(lambda x: -1, range(256))

    for i in range(0, len(tBytes)):
      tVal = struct.unpack('B', tBytes[i])[0]
      tailSignature[i + (self.offset - len(tBytes))][tVal] = 1

    for i in range(len(tBytes), self.offset):
      tailSignature[i] = map(lambda x: -1, range(256))

    self._signature = (headSignature, tailSignature)

  def compute(self, hBytes, tBytes):

    if len(hBytes) < self.offset or len(tBytes) < self.offset:
      return self.__handleSmallFiles(hBytes, tBytes)

    headSignature = [ [0 for x in range(256)] for x in range(self.offset) ]
    tailSignature = [ [0 for x in range(256)] for x in range(self.offset) ]

    for i in range(0, self.offset):
      hVal = struct.unpack('B', hBytes[i])[0]
      headSignature[i][hVal] = 1

      tVal = struct.unpack('B', tBytes[i])[0]
      tailSignature[i][tVal] = 1

    self._signature = (headSignature, tailSignature)

  def signature(self):
    return self._signature

  def __str__(self):
    arrayToString   = lambda x: ",".join(map(str, x))
    matrixToString  = lambda m: "\n".join(map(arrayToString, m))

    return "{0}\n{1}\n{2}".format(
      self.offset,
      matrixToString(self._signature[0]),
      matrixToString(self._signature[1]),
    )
