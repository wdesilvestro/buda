"""
BUDA's Main File

This file is a command line wrapper for BUDA's library.
"""

import argparse
import library as lib


# Handle command line arguments
parser = argparse.ArgumentParser(description="A command-line utility to programmatically parse .txt files with XML"
                                             "templates.")
parser.add_argument('template_dir', action="store")
parser.add_argument('in_dir', action="store")
parser.add_argument('out_dir', action="store")
parser.add_argument('-a', action="store_true", dest="aggregate")
args = parser.parse_args()


# Access library and run appropriate functions
if args.aggregate:
    lib.parse_directory(args.template_dir, args.in_dir, args.out_dir, True)
else:
    lib.parse_directory(args.template_dir, args.in_dir, args.out_dir, False)