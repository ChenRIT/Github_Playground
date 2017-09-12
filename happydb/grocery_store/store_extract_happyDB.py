# Entity Extraction from HappyDB data
# This code needs to be reviewed and rewritten

import sys
from collections import Counter
import pandas as pds

# Read the happyDB sample file
data = pds.read_csv("/Users/chen/Research/Code/happiness-dataset-collection/data/cleaned/cleaned_hm.csv")
data_sub = data

#print(data.head())
store_mention = Counter()
with open("/Users/chen/grocery_stat.txt", 'w') as ofile:
    for i in range(0, data_sub['cleaned_hm'].size-1):
        if 'Walmart' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Walmart'] += 1
        elif 'Costco' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Costco'] += 1
        elif 'CVS' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['CVS'] += 1
        elif 'BJ' in data_sub['cleaned_hm'].iloc[i]:            
            store_mention['BJ'] += 1
        elif 'Kroger' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Kroger'] += 1            
        elif 'Harris Teeter' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Harris Teeter'] += 1            
        elif 'Hyvee' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Hyvee'] += 1                        
        elif 'Publix' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Publix'] += 1                        
        elif 'Ralphs' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Ralphs'] += 1                        
        elif 'Target' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Target'] += 1                        
        elif 'Trader Joe' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Trader Joe'] += 1                        
        elif 'Vons' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Vons'] += 1                        
        elif 'Whole Food' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Whole Food'] += 1                        
        elif 'Winn Dixie' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Winn Dixie'] += 1                        
        elif 'Safeway' in data_sub['cleaned_hm'].iloc[i]:
            store_mention['Safeway'] += 1                                    
#           ofile.write(data_sub['cleaned_hm'].iloc[i] + '\n')

store_mention_dict = dict(store_mention)
for (ind, val) in store_mention_dict.items():
    print (ind, val)
