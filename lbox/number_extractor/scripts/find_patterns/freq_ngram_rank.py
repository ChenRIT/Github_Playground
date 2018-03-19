# Find the most common ngrams in a text file

import spacy
import csv
from collections import Counter

nlp = spacy.load('en_core_web_sm')

def extract_ngrams(input_texts, window_size, pre_pad_num=100, post_pad_num=100):
    """ Extract the sentences containing "$"+Arabic numberals

    @parameters:
    window_size: the window size of the ngram. window_size represents the number of tokens to the left/right of the extracted number

    @return: the number of instances found
    """

    ins_count = 0

    # Find all character sequences that contain "price" or its capitalized format.
    reg_exp = ".{" + str(pre_pad_num) + "}price.{" + str(post_pad_num) + "}"
    print("Search for patterns: " + reg_exp)
    results = re.findall(reg_exp, input_texts, re.I|re.S)

    ngram_list = []
    # Process each result
    for res in results:
        doc = nlp(res)
        num_chunks = extract_num_chunk(res)
        for num in num_chunks:
            # Extract ngrams
            num_start, num_end = num
            ngram_start = None
            ngram_end = None
            if num_start > 0:
                ngram_start = num_start - window_size
            else:
                ngram_start = num_start

            if num_end < len(doc):
                ngram_end = num_end + window_size
            else:
                ngram_end = num_end

            # Replace the number with a special symbol
            ngram = doc[ngram_start:ngram_end]
            number = doc[num_start:num_end]
            ngram_text = ngram.text
            # print("ngram_text: {}".format(ngram_text))
            # print("type of ngram_text: {}".format(type(ngram_text)))            
            number_text = number.text
            # print("number_text: {}".format(number_text))
            # print("type of number_text: {}".format(type(number_text)))
            # print("Find: {}".format(ngram_text.find('200')))
            ngram_replace = ngram_text.replace(number_text, 'NUM')
            print("Text after replacement: {}".format(ngram_replace))

            ngram_list.append(ngram_replace)

    return ngram_list

if __name__ == "__main__":
    # Read input file
    input_file = "./test.txt"
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
    top_one_hundred = ngram_counter.most_common(100)
    
    with open(output_file, "w") as ofile:
        sentwriter = csv.writer(ofile)
        sentwriter.writerow(['index', 'pattern', 'Lb', 'Ub', 'Unit', 'Rate'])
        row_idx = 0
        for (gram, count) in top_one_hundred:
            sentwriter.writerow([row_idx, gram])
            row_idx += 1


        
