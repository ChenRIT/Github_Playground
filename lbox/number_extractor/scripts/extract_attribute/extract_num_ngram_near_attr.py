# Extract common ngrams and rank them

import argparse
from collections import deque
from collections import Counter

import spacy
from spacy.symbols import NUM, PUNCT, SPACE

nlp = spacy.load('en')

def get_closest_num(doc, token_idx):
    '''
    Get the index of the closest NUM token near token_idx

    @return:
    a tuple (position, idx):
    position: a boolean that indicates whether NUM is to the left or right. {True: left, False: right)
    idx: the idx of the NUM token
    '''
    gap = 1
    for i in range(0, 1000):
        right_idx = token_idx + gap
        left_idx = token_idx - gap
        if doc[right_idx].pos == NUM:
            return (False, right_idx)
        elif doc[left_idx].pos == NUM:
            return (True, left_idx)
        else:
            gap += 1

    return (False, 0)

def get_ngrams(doc, start_idx, end_idx, gram_num):
    '''
    Get the ngrams that include the number that starts at start_idx and ends at end_idx
    '''
    igrams = []
    #print("start idx: {}, end idx: {}".format(start_idx, end_idx))
    #print("gram_num: {}".format(gram_num))
    for i in range(0, gram_num):
        left_window = i
        right_window = gram_num - i - 1
        gram_start = start_idx - left_window
        gram_end = end_idx + right_window
        #print("start: {}, end: {}".format(gram_start, gram_end))
        gram = ""
        has_punct = False
        for j in range(gram_start, gram_end+1):
            # Do not consider ngrams with punctuation
            if doc[j].pos == PUNCT:
                has_punct = True
                break
            
            if j < start_idx or j > end_idx:
                gram += doc[j].text + " "
            elif j == start_idx:
                gram += "NUM "
            else:
                continue
        if has_punct:
            continue
        
        #print(gram)
        igrams.append(gram)
    return igrams

def get_ngram_left(doc, end_idx, max_gram):
    '''
    Get the ngrams of a number to the left of the attribute
    '''
    start_idx = None
    cur_idx = end_idx - 1
    for i in range(0, 1000):
        if doc[cur_idx].pos == NUM:
            cur_idx -= 1
            continue
        else:
            start_idx = cur_idx + 1

    #print("start idx: {}, end idx: {}".format(start_idx, end_idx))
    ngrams = []
    for i in range(2, max_gram+1):
        igrams = get_ngrams(doc, start_idx, end_idx, i)
        ngrams = ngrams + igrams
    return ngrams

def get_ngram_right(doc, start_idx, max_gram):
    '''
    Get the ngrams of a number to the right of the attribute
    '''
    end_idx = None
    cur_idx = start_idx + 1
    for i in range(0, 1000):
        if doc[cur_idx].pos == NUM:
            cur_idx += 1
            continue
        else:
            end_idx = cur_idx - 1

    ngrams = []
    for i in range(2, max_gram+1):
        igrams = get_ngrams(doc, start_idx, end_idx, i)
        ngrams = ngrams + igrams
    return ngrams

def rank_ngrams(fname, max_gram, top_n=10):
    '''
    Rank the ngrams containing numerical values in the input file
    '''
    doc = None
    with open(fname) as ifile:
        doc = nlp(ifile.read())

    ngrams = []
    for token in doc:
        if token.text == "ATTR":
            position, closest_num_idx = get_closest_num(doc, token.i)
            if position == True:
                left_ngrams = get_ngram_left(doc, closest_num_idx, max_gram)
                ngrams = ngrams + left_ngrams
                #print("left_ngrams: {}".format(left_ngrams))
            else:
                right_ngrams = get_ngram_right(doc, closest_num_idx, max_gram)
                ngrams = ngrams + right_ngrams
                #print("right_ngrams: {}".format(right_ngrams))                
    #print("ngrams: {}".format(ngrams))
    ngram_ranker = Counter(ngrams)
    return ngram_ranker


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
        #print(rank_results)
        # for ele in rank_results.keys():
        #     print(str(ele) + '\n')
        #results = list(rank_results.keys())[:top_n]
        results = rank_results.keys()
        #print(results)
        combined_results.append(results)

    # Find common patterns that appear for all attributes
    #print("Combined results: {}".format(combined_results))
    assert len(combined_results) > 1    
    common_pattern = set(combined_results[0]).intersection(set(combined_results[1]))

    for res in combined_results[2:]:
        common_pattern = common_pattern.intersection(set(res))
    print(common_pattern)
            
