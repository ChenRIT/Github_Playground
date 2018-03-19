# Find the most common ngrams in a text file

import argparse
import spacy
import csv
from collections import Counter

nlp = spacy.load('en_core_web_sm')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", type=str, help="The input file name", default="./text.txt")
    parser.add_argument("-top", type=int, help="The number of common patterns to be output", default=100)    
    args = parser.parse_args()

    input_file = args.dir
    top_num = args.top
    output_file = "ngram_rank_result.csv"

    lower_ngram = 2
    upper_ngram = 5

    # Obtain ngrams from all sentences
    # Normalize numbers
    ngram_list = []
    with open(input_file) as ifile:
        for line in ifile:
            parse_line = nlp(line)
            if len(line) < lower_ngram:
                continue
            
            # Enumerate all possible ngrams
            for start_idx in range(len(parse_line)):
                for gram_num in range(lower_ngram, upper_ngram+1):
                    end_idx = start_idx + gram_num
                    if end_idx > len(parse_line):
                        break

                    new_gram = ""
                    num_idx = 1
                    has_num = False
                    # Normalize numbers
                    for token in parse_line[start_idx:end_idx]:
                        if token.pos == spacy.symbols.NUM:
                            new_gram += "NUM_" + str(num_idx) + " "
                            has_num = True
                            num_idx += 1
                        else:
                            new_gram += token.text + " "

                    if not has_num:
                        continue
                    
                    new_gram = new_gram.rstrip() # Remove the trailing white spaces
                    if new_gram.endswith("."):
                        continue

                    ngram_list.append(new_gram)

    # Count and rank the ngrams
    ngram_counter = Counter(ngram_list)

    # Output the ranked ngrams into an csv file
    top_one_hundred = ngram_counter.most_common(top_num)
    
    with open(output_file, "w") as ofile:
        sentwriter = csv.writer(ofile)
        sentwriter.writerow(['index', 'pattern', 'Lb', 'Ub', 'Unit', 'Rate'])
        row_idx = 0
        for (gram, count) in top_one_hundred:
            sentwriter.writerow([row_idx, gram])
            row_idx += 1


        
