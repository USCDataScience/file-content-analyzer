##Byte Frequency Analysis

```python
from rw.reader import *
from bfa.bfa import *

reader = FileReader(" PATH TO FILE ")
analyzer = BFAnalyzer()

reader.read(analyzer.compute)
print analyzer.clean()
```

##Byte Frequency Correlation

```python
from bfc.bfc import *

fs = BFCorrelator(baseSignature)
print fs.correlate(compareWith)
```

## Getting the data

[Use RIOFS](https://github.com/skoobe/riofs)
Mount the given S3 bucket onto local folder

While invoking download.py pass MOUNT_POINT and END_POINT as command line arguments.

The script traverses the bucket via DFS and checks the file-type of each file
with tika and then copies it to your local directory

```
# Start the tika rest server in the background
tika-rest-server

# Start the download script
python download.py <MOUNT_POINT> <END_POINT>

# To count the number of files of each type
find <END_POINT> -type f | sed 's%/[^/]*$%%' | sort | uniq -c
```

Progressive file download: Tika server is inherently multi-threaded. So parallilizing the download
process reduces the download time considerably. Using python `multiprocess` download and parsing
of the files from the S3 bucket can be parallilized. Initial investigation revieled that `com/` and
`org/` are the 2 biggest subfolders in the S3 bucket. Thus 3 seperate python processes each for the
contents of com, org and all the other folders is an optimal download strategey. Each python process
parallilizes with 5 threads each.

```
python -u progressive.py <MOUNT_POINT>/org <END_POINT>/org progress-org.log > progress-org-op.log & disown
python -u progressive.py <MOUNT_POINT>/com <END_POINT>/com progress-com.log > progress-com-op.log & disown
python -u progressive.py <MOUNT_POINT>/other <END_POINT>/other progress-other.log > progress-other-op.log & disown
```
