import math

class compareFHT:
	def __init__(size,matrix,fingerprint):
		self.size=size
		self.matrix=matrix
		self.fingerprint=matrix

	def compare(self):
		sum=0
		denom=0
		for i in range(size):
			for j in range(256):
				sum=sum+ self.matrix[i][j]*self.fingerprint[i][j]
				denom=denom+self.fingerprint[i][j]

	return (sum/denom)
