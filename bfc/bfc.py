import math

SIGMA = 0.0035
SIGMA_SQR = SIGMA * SIGMA

class ByteFrequencyCorrelator:
  def __init__(self, baseSignature):
    self.baseSignature = baseSignature

  def correlate(self, signature):
    correlation = [None] * 256

    for i in range(256):
      diff = signature[i] - self.baseSignature[i]
      exp = ( -1 * diff * diff ) / ( 2 * SIGMA_SQR )
      correlation[i] = math.exp(exp)

    return correlation



