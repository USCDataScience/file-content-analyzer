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

