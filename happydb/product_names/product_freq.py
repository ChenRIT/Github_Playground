# Count the frequency of common product names in HappyDB

import sys
import argparse

from collections import Counter
import pandas as pds

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ipath", help="Path of the input file", default="/Users/chen/Research/Playground/Github_Playground/happydb/data/cleaned_hm.csv")
args = parser.parse_args()

# Read the happyDB sample file
input_file = args.ipath
data = pds.read_csv(input_file)

# Calculate the appearance frequency of common product names
prod_count = Counter()
for i in range(0, data['cleaned_hm'].size-1):
    if 'buy' in data['cleaned_hm'].iloc[i] or \
       'bought' in data['cleaned_hm'].iloc[i] or \
       'purchase' in data['cleaned_hm'].iloc[i] or \
       'order' in data['cleaned_hm'].iloc[i]:
        # if 'vehicle' in data['cleaned_hm'].iloc[i]:
        #     prod_count['vehicle'] += 1
        # elif 'bike' in data['cleaned_hm'].iloc[i] or \
        #      'bicycle' in data['cleaned_hm'].iloc[i]:
        #     prod_count['bike'] += 1
        # elif 'car' in data['cleaned_hm'].iloc[i]:
        #     prod_count['car'] += 1
        # elif 'phone' in data['cleaned_hm'].iloc[i]:
        #     prod_count['phone'] += 1
        # elif 'shirt' in data['cleaned_hm'].iloc[i]:
        #     prod_count['shirt'] += 1
        # elif 'tea' in data['cleaned_hm'].iloc[i]:
        #     prod_count['tea'] += 1
        # elif 'flower' in data['cleaned_hm'].iloc[i]:
        #     prod_count['tea'] += 1
        # elif 'shoe' in data['cleaned_hm'].iloc[i]:
        #     prod_count['shoe'] += 1
        if 'coffee' in data['cleaned_hm'].iloc[i]:
            prod_count['coffee'] += 1

prod_count_dict = dict(prod_count)
print ("product name", "frequency")
for (ind, val) in prod_count_dict.items():
    print (ind, val)
