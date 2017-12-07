#!/bin/bash

# This script assumes that Python 3 and pdfminer.six are installed system wide.

# The script should be placed within the same directory as pdfminer's pdf2txt.py file (provided within BUDA's files) and
# where all the .pdf files to be converted are located. Outputted .txt files will also be placed in this same directory.

for file in *.pdf;

do python3 pdf2txt.py -o "${file%.pdf}.txt" "$file";

done
