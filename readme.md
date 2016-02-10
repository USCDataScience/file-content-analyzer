##Byte Frequency Analysis

```python
from io.reader import *
from bfa.bfa import *

reader = FileReader(" PATH TO FILE ")
analyzer = ByteFrequencyAnalyzer()

reader.read(analyzer.compute)
print analyzer.clean()

```
