import math

SIGMA = 0.0035
SIGMA_SQR = SIGMA * SIGMA

class ByteFrequencyCorrelator:
  def __init__(self, baseSignature):
    self.baseSignature = baseSignature

  def correlate(self, signature):
    self.cmpSignature = signature

    self.correlation = [None] * 256

    for i in range(256):
      diff = self.cmpSignature[i] - self.baseSignature[i]
      exp = ( -1 * diff * diff ) / ( 2 * SIGMA_SQR )
      self.correlation[i] = math.exp(exp)

    return self.correlation

  def __str__(self):
    f1 = ",".join(map(str, self.baseSignature))
    f2 = ",".join(map(str, self.cmpSignature ))
    c  = ",".join(map(str, self.correlation  ))

    return "{0}\n{1}\n{2}".format(f1, f2, c)
