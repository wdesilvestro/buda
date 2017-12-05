# Testing out some functions that will be refactored later

import library as lib
import argparse


# Parse command-line arguments
parser = argparse.ArgumentParser(description="A command-line utility to programmatically parse .txt files with XML templates.")
parser.add_argument('template_dir', action="store")
parser.add_argument('in_dir', action="store")
parser.add_argument('out_dir', action="store")
parser.add_argument('-a', action="store_true", dest="aggregate")

args = parser.parse_args()


# Access library and run appropriate functions
if args.aggregate:
    lib.parse_aggregate(args.template_dir, args.in_dir, args.out_dir)
else:
    lib.parse_individual(args.template_dir, args.in_dir, args.out_dir)