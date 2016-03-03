import struct
import math

class BFAnalyzer:
  def __init__(self):
    self.__frequency = map(lambda x: float(0), range(256))

  def compute(self, byte):
    val = struct.unpack('B', byte)[0]
    self.__frequency[val] = self.__frequency[val] + 1

  def smoothen(self):
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

  # http://www.forensicswiki.org/w/images/f/f9/Mcdaniel01.pdf
  def compand(self):
    B = 1.5
    self.__frequency =  map(lambda x: x ** ( 1 / B), self.__frequency)
    return self

  def frequency(self):
    return self.__frequency

  def __str__(self):
    return ",".join(map(str, self.__frequency))
