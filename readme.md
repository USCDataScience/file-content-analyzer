## Analysis Interface

CSCI-599 Spring 2016 - Team 1, Assignment 1

###Byte Frequency Analysis

```python
from rw.reader import *
from bfa.bfa import *

reader = FileReader(" PATH TO FILE ")
analyzer = BFAnalyzer()

reader.read(analyzer.compute)
print analyzer.clean()

# COMPANDING FN: x ^ ( 1 / 1.5 )
# http://www.forensicswiki.org/w/images/f/f9/Mcdaniel01.pdf
```

###Byte Frequency Correlation

```python
from bfc.bfc import *

fs = BFCorrelator(baseSignature)
print fs.correlate(compareWith)
```

###Byte Frequency Cross-Correlation

```python
from bfa.cross import *

c = BFCrossCorrelator(signature)
print c.correlate()
```

###File Header Trailer Analysis

```python
from fht.fht import *

# OFFSET -> user defined integer
r = HTFileReader(" PATH TO FILE ", OFFSET)
fht = FHTAnalyzer(OFFSET)
r.read(fht.compute)
print fht.signature()
```

###File Header Trailer Assurance Level

```python
from fht.fht import *
from fht.compare import *

cm = CompareFHT(fht1.signature(), fht2.signature())
print cm.correlate()
print cm.assuranceLevel()

# Note: Assurance level returns the __MEAN__ not the __MAX__ as specified here.
```
***

## Getting the data

The [Trec-Polar](https://github.com/chrismattmann/trec-dd-polar) data set contains data in the
common crawl format. It's available on S3.

###Step 1: Download Interface

[Use RIOFS](https://github.com/skoobe/riofs)
Mount the given S3 bucket onto local folder

While invoking download.py pass MOUNT_POINT and END_POINT as command line arguments.

The script traverses the bucket via DFS and checks the file-type of each file
with tika and then copies it to your local directory

```
# Start the download script
python download.py <MOUNT_POINT> <END_POINT>

# To count the number of files of each type
find <END_POINT> -type f | sed 's%/[^/]*$%%' | sort | uniq -c
```

###Step 2: Parallelizing Download

__Progressive file download (MAP Phase):__
Tika server is inherently multi-threaded. So parallelizing the download
process reduces the download time considerably. Using python `multiprocess` download and parsing
of the files from the S3 bucket can be parallelized. Initial investigation reviled that `com/`,
`org/`, `gov/` and `edu/` are the 2 biggest sub folders in the S3 bucket.

Thus 4 separate python processes each for the contents of the mentioned folder
and one for all the other folders is an optimal download strategy. Each python process
parallelizes with 5 threads each.

```bash
cd ./download
python -u progressive.py <MOUNT_POINT>/org <END_POINT>/org progress-org.log > progress-org-op.log > /dev/null &
python -u progressive.py <MOUNT_POINT>/com <END_POINT>/com progress-com.log > progress-com-op.log > /dev/null &
python -u progressive.py <MOUNT_POINT>/org <END_POINT>/org progress-org.log > progress-org-op.log > /dev/null &
python -u progressive.py <MOUNT_POINT>/edu <END_POINT>/edu progress-edu.log > progress-edu-op.log > /dev/null &
python -u progressive.py <MOUNT_POINT>/other <END_POINT>/other progress-other.log > progress-other-op.log > /dev/null &

# To display download errors
cat *-op.log | grep "ERROR"
```

__Accumulating results (Reduce Phase):__
Once the 5 individual folders are downloaded completely they can be grouped into one collection using the
`group.py` script.

```bash
python group.py <PATH TO PARENT FOLDER>
```

###Step 3: Cleaning Data

The application-octet stream folder contained a lot of empty files. The `empty.py` script bins these empty files
separately.

***

##Signature Computation

We leveraged python `multiprocess` BFA and FHT signature computation using a 2 phased Map-Reduce approach.

###BFA

1. Map Phase: A pool of n threads compute signatures for files in a given bin and write the file-size and signatures
into a CSV output file. (`batch/bfa.py`)
2. Reduce Phase: A python program reads the file line by line and computes the average of each signature.
(`batch/bfa_aggreagte.py`) __Note:__ This only uses 75% of the signatures to compute the average. For types with
fewer than 5 files all the signatures are used.

####Size Clustering

The `r/size-summary.r` script reads the generated signature files and runs k-means clustering based on the file-sizes
for a given type. It also generates jpeg plots for the file-size variations for each cluster.

The `batch/bfa_size_aggreagate.py` script reads the output generated from `size-summary.r` and computes average signatures
for each size-cluster for a given file type. __Note:__ This only happens for types with no fewer than 5 unique signatures.


###FHT

1. Map Phase: A pool of n threads read the first and last 4,8 and 16 bytes of all the files in a given bin and store them
onto 3 separate files. (`batch/fht.py`)
2. Reduce Phase: A python program reads these files 16,32 and 64 bits at a time and computes the aggregate FHT signature.
(`batch/fht_aggreagte.py`)


***

##Visualizing Results

A separate grunt angular application has been built to visualize these results. The `visualize.py` script computes
BFA, BFC, Cross-Correlation and FHT on given files and produces signatures in a format readable by the web-app.

__Note:__ The generated signatures need to be moved into the /data folder in the webapp after computation.

```bash
python visualize.py bfa <FilePath>
python visualize.py bfc <FilePath1> <FilePath2>
python visualize.py bfcc <FilePath>
python visualize.py fht <FilePath>
```
