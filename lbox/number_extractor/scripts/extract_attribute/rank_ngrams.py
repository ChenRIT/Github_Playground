# Extract common ngrams and rank them

import argparse
from collections import deque
from collections import Counter

import spacy
from spacy.symbols import NUM, PUNCT, SPACE

nlp = spacy.load('en')

def rank_ngrams(fname, gram_num, top_n=10):
    '''
    Rank the ngrams in the input file
    '''
    gram_holder = []
    ngram_result = []
    for i in range(0, gram_num):
        gram_holder.append(deque())

    
    with open(fname) as ifile:
        doc = nlp(ifile.read())
        for token in doc:
            # print(gram_holder)
            if token.pos == PUNCT or token.pos == SPACE:
                continue
            
            for i in range(0, len(gram_holder)):
                # Update each ngram bucket
                if len(gram_holder[i]) < (i+1):
                    gram_holder[i].append(token.text)
                else:
                    gram_holder[i].append(token.text)
                    gram_holder[i].popleft()
            for i in range(0, len(gram_holder)):
                # Collect all ngrams containing number
                if len(gram_holder[i]) == (i+1) and gram_holder[i].count("NUM") > 0:
                    igram = ""
                    for word in gram_holder[i]:
                        igram += word + " "
                    ngram_result.append(igram)
                    #print("Found: {}\n".format(igram))
            ngram_ranker = Counter(ngram_result)
    return ngram_ranker.most_common(top_n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ifnames", nargs='+', help="The data files to be opened.")
    #parser.add_argument("-ofname", type=str, help="The output file to be opened.", default="test_output.txt")
    parser.add_argument("-gn", "--gramnum", type=int, help="The maximum number of grams to be considered.", default=4)
    parser.add_argument("-top", type=int, help="The top n number of patterns to be considered.", default=10)    
    args = parser.parse_args()

    ifnames = args.ifnames
    gram_num = args.gramnum
    top_n = args.top
    combined_results = []
    for fname in ifnames:
        rank_results = rank_ngrams(fname, gram_num, top_n)
        print(rank_results)
        results = list(rank_results)
        #print(results)
        combined_results.append(results)

    # Find common patterns that appear for all attributes
    assert len(combined_results) > 1    
    common_pattern = set(combined_results[0]).intersection(set(combined_results[1]))

    for res in combined_results[2:]:
        common_pattern = common_pattern.intersection(set(res))
    print(common_pattern)
            
