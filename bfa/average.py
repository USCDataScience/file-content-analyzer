import math

class BFAverage:
  def __init__(self, signature, count):
    self._signature = signature
    self._count = count

  def accumulate(self, cmpSignature):
    newSignature = map(lambda i: (self._count * self._signature[i] + cmpSignature[i]) / ( self._count + 1 ), range(256))
    return BFAverage(newSignature, self._count+1)

  def signature(self):
    return self._signature
