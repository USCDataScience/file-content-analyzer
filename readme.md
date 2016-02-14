##Byte Frequency Analysis

```python
from rw.reader import *
from bfa.bfa import *

reader = FileReader(" PATH TO FILE ")
analyzer = ByteFrequencyAnalyzer()

reader.read(analyzer.compute)
print analyzer.clean()
```

##Byte Frequency Correlation

```python
from bfc.bfc import *

fs = ByteFrequencyCorrelator(baseSignature)
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

