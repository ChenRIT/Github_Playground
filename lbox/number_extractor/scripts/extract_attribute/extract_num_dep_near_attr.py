# Extract common ngrams around the number closest to the attribute and rank them

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
        if right_idx < len(doc) and doc[right_idx].text == "NUM":
            return (False, right_idx)
        elif left_idx > 0 and doc[left_idx].text == "NUM":
            return (True, left_idx)
        else:
            gap += 1

    return (False, 0)

def get_dep_exp(doc, num_idx, depth=3):
    '''
    Obtain expressions that surrounds a number based on dependency parsing
    '''
    exps = []
    root = doc[num_idx]
    for i in range(0, depth):
        word_list = [child.text for child in root.subtree]
        exp_num = " ".join(word_list)
        exps.append(exp_num)
        if root == root.head:
            break
        root = root.head
    return exps

def rank_ngrams(fname, max_gram, top_n=10):
    '''
    Rank the ngrams containing numerical values in the input file
    '''
    doc = None
    with open(fname) as ifile:
        doc = nlp(ifile.read())

    expressions = []
    for token in doc:
        if token.text == "ATTR":
            _, closest_num_idx = get_closest_num(doc, token.i)
            exps_num = get_dep_exp(doc, closest_num_idx)
            expressions = expressions + exps_num
    ngram_ranker = Counter(expressions)
    return ngram_ranker

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ifnames", nargs='+', help="The data files to be opened.")
    #parser.add_argument("-ofname", type=str, help="The output file to be opened.", default="test_output.txt")
    parser.add_argument("-gn", "--gramnum", type=int, help="The maximum number of grams to be considered.", default=4)
    parser.add_argument("-top", type=int, help="The top n number of patterns to be considered.", default=10)    
    args = parser.parse_args()

    ifnames = args.ifnames
    #cfname = args.colorfname
    gram_num = args.gramnum
    top_n = args.top
    combined_results = []
    for fname in ifnames:
        rank_results = rank_ngrams(fname, gram_num, top_n)
        #print(rank_results)
        # for ele in rank_results.keys():
        #     if "more than" in ele:
        #         print("{}: {}".format(ele, rank_results[ele]))
        # print("------------------\n\n")
        # results = list(rank_results.keys())[:top_n]
        #filtered_results = [key for (key, value) in rank_results.items() if value > 1]
        results = rank_results.keys()
        print(str(results) + "\n")
        combined_results.append(results)
        #combined_results.append(filtered_results)


    # Find common patterns that appear for all attributes
    #print("Combined results: {}".format(combined_results))
    assert len(combined_results) > 1    
    common_pattern = set(combined_results[0]).intersection(set(combined_results[1]))

    for res in combined_results[2:]:
        common_pattern = common_pattern.intersection(set(res))

    print("# of patterns found: {}".format(len(common_pattern)))
    print(*common_pattern, sep='\n')
            
