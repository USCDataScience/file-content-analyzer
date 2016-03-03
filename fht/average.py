import math

class FHTAverage:
  def __init__(self, fingerprint, count):
    self._fingerprint = fingerprint
    self._count = count

    self.offset = len(fingerprint[0])

  def accumulate(self, fht):
    head  = [ [0 for x in range(256)] for x in range(self.offset) ]
    trail = [ [0 for x in range(256)] for x in range(self.offset) ]

    for i in range(self.offset):
      for j in range(256):
        head[i][j] = ( self._count * float(self._fingerprint[0][i][j]) + fht[0][i][j] ) / ( self._count + 1 )
        trail[i][j] = ( self._count * float(self._fingerprint[1][i][j]) + fht[1][i][j] ) / ( self._count + 1 )

    return FHTAverage((head, trail), self._count+1)

  def fingerprint(self):
    return self._fingerprint

  @staticmethod
  def getInstance(offset):
    initHead = [ [0 for x in range(256)] for x in range(offset) ]
    initTrail = [ [0 for x in range(256)] for x in range(offset) ]
    return FHTAverage((initHead, initTrail), 0)

  def __str__(self):
    arrayToString   = lambda x: ",".join(map(str, x))
    matrixToString  = lambda m: "\n".join(map(arrayToString, m))

    return "{0}\n{1}\n{2}".format(
      self.offset,
      matrixToString(self._fingerprint[0]),
      matrixToString(self._fingerprint[1]),
    )
