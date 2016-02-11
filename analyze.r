library('rPython')
library('gsubfn')
library('corrplot')

python.load("/Users/nithinkrishna/projects/content/analytics-engine/bfa/bfa.py")
python.load("/Users/nithinkrishna/projects/content/analytics-engine/bfc/bfc.py")
python.load("/Users/nithinkrishna/projects/content/analytics-engine/bfcc/bfcc.py")
python.load("/Users/nithinkrishna/projects/content/analytics-engine/io/reader.py")

byte_frequency <- function(file_name){
  cmd <- fn$identity("r1 = FileReader('`file_name`')")
  python.exec(cmd)
  python.exec("a1 = ByteFrequencyAnalyzer()")
  python.exec("r1.read(a1.compute)")
  byte_frequency = python.call("a1.smoothen")
  names(byte_frequency) <- c(1:256)
  return(byte_frequency)
}

byte_frequency_correlation <- function(f1, f2){
  cmd <- fn$identity("r1 = FileReader('`f1`')")
  python.exec(cmd)
  python.exec("a1 = ByteFrequencyAnalyzer()")
  python.exec("r1.read(a1.compute)")
  cmd <- fn$identity("r2 = FileReader('`f2`')")
  python.exec(cmd)
  python.exec("a2 = ByteFrequencyAnalyzer()")
  python.exec("r2.read(a2.compute)")
  python.exec("c = ByteFrequencyCorrelator(a1.smoothen())")
  python.exec("sig  = a2.smoothen()")
  python.exec('cor = c.correlate(sig)')
  correlation = python.get("cor")
  names(correlation) <- c(1:256)
  return(correlation)
}


byte_frequency_cross_correlation <- function(file_name){
  cmd <- fn$identity("r1 = FileReader('`file_name`')")
  python.exec(cmd)
  python.exec("a1 = ByteFrequencyAnalyzer()")
  python.exec("r1.read(a1.compute)")
  python.exec("c = ByteFrequencyCrossCorrelator(a1.smoothen())")
  python.exec("lst = reduce(lambda x,y: x+y, c.correlate())")
  correlation = python.get("lst")
  return(matrix(correlation, 256, 256))
}


pdf1 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/1.pdf")
pdf2 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/2.pdf")
pdf3 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/3.pdf")

html1 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/1.html")
html2 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/2.html")
html3 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/3.html")

ppt1 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/1.ppt")
ppt2 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/2.ppt")
ppt3 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/3.ppt")

mp41 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/1.mp4")

txt1 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/1.txt")
txt2 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/2.txt")
txt3 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/3.txt")

jpg1 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/1.jpg")
jpg2 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/2.jpg")
jpg3 = byte_frequency("/Users/nithinkrishna/projects/content/analytics-engine/test/3.jpg")


barplot(pdf1)
barplot(pdf2)
barplot(pdf3)

cmp = byte_frequency_correlation(
  "/Users/nithinkrishna/projects/content/analytics-engine/test/1.pdf",
  "/Users/nithinkrishna/projects/content/analytics-engine/test/2.pdf"
)
barplot(cmp)

ccr = byte_frequency_cross_correlation("/Users/nithinkrishna/projects/content/analytics-engine/test/1.pdf")
corrplot(cor(ccr), method = "square")
image(ccr)
persp(ccr, expand=0.2)
contour(ccr)
