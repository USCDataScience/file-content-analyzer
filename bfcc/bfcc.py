import math

SIGMA = 0.0035
SIGMA_SQR = SIGMA * SIGMA

class ByteFrequencyCrossCorrelator:
  def __init__(self, baseSignature):
    self.baseSignature = baseSignature

  def correlate(self):
    correlation = Matrix = [[0 for x in range(256)] for x in range(256)]

    for i in range(256):
      for j in range(i):
        freqDiff = ( self.baseSignature[i] - self.baseSignature[j] )
        exp = ( -1 * freqDiff * freqDiff ) / ( 2 * SIGMA_SQR )

        correlation[i][j] = freqDiff
        correlation[j][i] = math.exp(exp)

    return correlation




