# Entity Extraction from HappyDB data
# This code needs to be reviewed and rewritten

import sys
import argparse

import pandas as pds

parser = argparse.ArgumentParser()
parser.add_argument("--ipath", type=str, help="The path of the input file", default="/Users/chen/default_hm.csv")
parser.add_argument("--opath", type=str, help="The path of the output file", default="/Users/chen/default_purchase.txt")
args = parser.parse_args()

# Read the happyDB sample file
input_file = args.ipath
data = pds.read_csv(input_file)
data_sub = data

# Find all lines containing "buy", "purchase" or "bought" etc.
output_file = args.opath
with open(output_file, 'w') as ofile:
    for i in range(0, data_sub['cleaned_hm'].size-1):
        if 'buy' in data_sub['cleaned_hm'].iloc[i] or \
           'bought' in data_sub['cleaned_hm'].iloc[i] or \
           'purchase' in data_sub['cleaned_hm'].iloc[i] or \
           'order' in data_sub['cleaned_hm'].iloc[i]:
           ofile.write(data_sub['cleaned_hm'].iloc[i] + '\n')
