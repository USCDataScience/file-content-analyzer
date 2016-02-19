import math
import pdb

class FHTAnalyzer:
  def __init__(self, offset):
    self.offset = offset

  def __handleSmallFiles(self, hBytes, tBytes):
    headSignature = [ [0 for x in range(256)] for x in range(self.offset) ]
    tailSignature = [ [0 for x in range(256)] for x in range(self.offset) ]

    for i in range(0, len(hBytes)):
      hVal = struct.unpack('B', hBytes[i])[0]
      headSignature[i][hVal] = 1

    for i in range(0, self.offset - len(hBytes)):
      headSignature[i + self.offset][hVal] = -1

    for i in range(0, len(tBytes)):
      tVal = struct.unpack('B', tBytes[i])[0]
      tailSignature[i + (self.offset - len(tBytes))][tVal] = 1

    for i in range(0, self.offset - len(tBytes)):
      tailSignature[i + self.offset][hVal] = -1

    return (headSignature, tailSignature)

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

    return(headSignature, tailSignature)
