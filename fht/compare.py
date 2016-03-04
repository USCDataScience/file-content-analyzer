class Comparator:
  def __init__(self, fingerprint, matrix):
    self.fingerprint = fingerprint
    self.matrix = matrix

    self.height = len(self.matrix)
    self.width = len(self.matrix[0])

    # Length of the offsets needs to match
    if len(self.matrix) != len(self.fingerprint):
      raise "Offsets don't match"

  def compare(self):
    correlation = [0 for x in range(self.height)]

    for i in range(self.height):
      total = sum(self.fingerprint[i])
      weightedSum = reduce(lambda m, j: m + ( float(self.matrix[i][j]) * float(self.fingerprint[i][j]) ), range(self.width), 0)

      correlation[i] = float(weightedSum) / float(total)

    return correlation

class CompareFHT:
  def __init__(self, fhtFingerprint, fhtFile):
    self.fhtFingerprint = fhtFingerprint
    self.fhtFile = fhtFile

    # Assuming both matrices are of the same dimension
    self.offset = len(self.fhtFingerprint[0])
    self._correlation = None

  def correlate(self):
    #Memoization
    if self._correlation != None:
      return self._correlation

    c1 = Comparator(self.fhtFingerprint[0], self.fhtFile[0]).compare()
    c2 = Comparator(self.fhtFingerprint[1], self.fhtFile[1]).compare()
    self._correlation = (c1, c2)
    return self._correlation

  def assuranceLevel(self):
    self.correlate()
    cor = self._correlation

    # Variation from what's listed in the paper
    al = max( sum(cor[0]) / len(cor[0]), sum(cor[0]) / len(cor[1]) )

    return al
