# Entity Extraction from HappyDB data
# This code needs to be reviewed and rewritten

import sys
import argparse

import pandas as pds

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ipath", type=str, help="The path of the input file", default="/Users/chen/Research/Playground/Github_Playground/happydb/data/cleaned_hm.csv")
parser.add_argument("-o", "--opath", type=str, help="The path of the output file", default="/Users/chen/default_books.txt")
args = parser.parse_args()

# Read the happyDB sample file
input_file = args.ipath
data = pds.read_csv(input_file)
data_sub = data

# Find all lines containing book-related verbs or nouns.
output_file = args.opath
book_count = 0
with open(output_file, 'w') as ofile:
    for i in range(0, data_sub['cleaned_hm'].size-1):
        if 'a book' in data_sub['cleaned_hm'].iloc[i] or \
           'the book' in data_sub['cleaned_hm'].iloc[i] or \
           'this book' in data_sub['cleaned_hm'].iloc[i] or \
           'that book' in data_sub['cleaned_hm'].iloc[i] or \
           'his book' in data_sub['cleaned_hm'].iloc[i] or \
           'her book' in data_sub['cleaned_hm'].iloc[i] or \
           'my book' in data_sub['cleaned_hm'].iloc[i] or \
           'fiction' in data_sub['cleaned_hm'].iloc[i] or \
           'biograph' in data_sub['cleaned_hm'].iloc[i]:
           #ofile.write(data_sub['cleaned_hm'].iloc[i] + '\n')
            book_count += 1

print(book_count)
