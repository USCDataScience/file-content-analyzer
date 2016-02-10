import struct
import math

class ByteFrequencyAnalyzer:
  def __init__(self):
    self.__frequency = map(lambda x: float(0), range(256))

  def compute(self, byte):
    val = struct.unpack('B', byte)[0]
    self.__frequency[val] = self.__frequency[val] + 1

  def clean(self):
    return (
      self
        .normalize()
        .compand()
        .frequency()
    )

  def normalize(self):
    norm = max(self.__frequency)
    self.__frequency =  map(lambda x: x / norm, self.__frequency)
    return self

  # A-LOG compander
  def compand(self):
    A = 87.6
    alog = lambda x: ( A * x ) / ( 1 + math.log(A, 10) ) if x < (1 / A) else ( 1 + math.log(A * x, 10) ) / ( 1 + math.log(A, 10) )
    self.__frequency =  map(alog, self.__frequency)
    return self

  def frequency(self):
    return self.__frequency
