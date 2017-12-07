# Testing out some functions that will be refactored later

import re

items = [re.A, re.ASCII, re.I, re.IGNORECASE, re.L, re.LOCALE, re.M, re.MULTILINE, re.S, re.DOTALL, re.X, re.VERBOSE]

test = {}

for item in items:
    test.update({str(item): int(item)})

print(153 | 12)