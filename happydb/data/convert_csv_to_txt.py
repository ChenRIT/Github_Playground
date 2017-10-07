# Convert a column of happyDB data to plain text

import sys
import pandas as pds

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ipath", type=str, default="/Users/chen/Research/Playground/Github_Playground/happydb/data/cleaned_hm.csv", help="The path of the input file")
parser.add_argument("--opath", type=str, default="/Users/chen/Research/Playground/Github_Playground/happydb/data/happyDB_clean.txt", help="The path to store the output file")
args = parser.parse_args()

# Read the happyDB sample file
input_path = args.ipath
data = pds.read_csv(input_path)
output_path = args.opath
with open(output_path, 'w') as ofile:
    for i in range(0, data['cleaned_hm'].size-1):    
        ofile.write("\t" + data['cleaned_hm'].iloc[i] + '\n')
