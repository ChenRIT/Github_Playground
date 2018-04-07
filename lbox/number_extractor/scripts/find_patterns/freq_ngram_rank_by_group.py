# Find the most common ngrams for each n in a text file

import argparse
import spacy
import csv
from collections import Counter

nlp = spacy.load('en_core_web_sm')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-fname", type=str, help="The input file name", default="./text.txt")
    parser.add_argument("-top", type=int, help="The number of common patterns to be output for each ngram group", default=30)    
    args = parser.parse_args()

    input_file = args.fname
    top_num = args.top
    output_file = "ngram_group_rank_result.csv"

    lower_ngram = 2
    upper_ngram = 5

    # Obtain ngrams from all sentences
    # Normalize numbers
    num_to_grams = {}
    for i in range(lower_ngram, upper_ngram+1):
        num_to_grams[i] = []
    
    with open(input_file) as ifile:
        for line in ifile:
            parse_line = nlp(line)
            if len(line) < lower_ngram:
                continue
            
            # Enumerate all possible ngrams
            for gram_num in range(lower_ngram, upper_ngram+1):
                sent_gram = []
                for start_idx in range(len(parse_line)):
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

                    sent_gram.append(new_gram)

                num_to_grams[gram_num] += sent_gram
                
                # # Count and select the top k grams
                # target_gram_counter = Counter(target_gram_list)
                # top_grams = target_gram_counter.most_common(top_num)
                # top_gram_list = [gram for (gram, count) in top_grams]

                # print("Top {} grams:".format(gram_num))
                # print(top_gram_list)                
                # ngram_list.append(top_gram_list)

    overall_top_ngrams = []
    for _,value in num_to_grams.items():
        filter_value = [val for val in value if ":" not in val]
        gram_count = Counter(filter_value)
        top_ngrams = gram_count.most_common(top_num)
        top_ngrams_list = [gram for (gram, count) in top_ngrams]
        overall_top_ngrams += top_ngrams_list
    
    with open(output_file, "w") as ofile:
        sentwriter = csv.writer(ofile)
        sentwriter.writerow(['index', 'pattern', 'Lb', 'Ub', 'Unit', 'Rate'])
        row_idx = 0
        for gram in overall_top_ngrams:
            sentwriter.writerow([row_idx, gram])
            row_idx += 1


        
