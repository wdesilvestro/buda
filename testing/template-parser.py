# Test creating my own parser

import re

def envelope(l):
    print(l)

# Load template file into memory
file = open("template.txt", "r")

for line in file.readlines():
    if line[0:3] == "%E%":
        envelope(line[3:])

file.close()