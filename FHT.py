import math

class FileHeaderTrailer:
	def __init__(self,baseSignature,no_of_files,byte,file1):
		self.baseSignature=baseSignature
		self.byte=byte
		self.file=file1
		self.prev_files=prev_files
	def fht(self):
		signature = Matrix= [[0 for x in range(256)]for x in range(self.byte)]
		size=len(self.file)
		for i in range(byte):
			for j in range(256):
				no= self.file.read(8)
				if(j==no):
					signature[i][j]=1
				else:
					signature[i][j]=0
				if(i>=size):
					signature[i][j]=-1

		newSignature=Matrix= [[0 for x in range(256)]for x in range(self.byte)]
		for i in range(byte):
			for j in range(256):
				newSignature=((baseSignature[i][j]*prev_files)+ signature[i][j])/(prev_files+1)


	return newSignature




