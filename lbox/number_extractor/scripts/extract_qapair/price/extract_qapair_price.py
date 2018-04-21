# Extract sentences following a question seeded by the questions about weight

from os import listdir
from os.path import isfile, join

import re
import argparse
import spacy
from spacy.symbols import NUM

import en_core_web_lg
nlp = en_core_web_lg.load()

def extract_sents(input_texts, output_file, verbose, post_pad_num=100):
    """ Extract the sentences containing question answer pairs

    @return: the number of instances found
    """

    ins_count = 0
    reg_exp = r"(?:(?:cost)|(?:price)).{,10}\?.{," + str(post_pad_num) + r"}"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.I)
    print("Find {} instances".format(len(results)))

    if verbose:
        print("The qualified sentences: ")
        for res in results:
            print("Res: {}".format(res))

    for res in results:
        #print("Matched sent: {}".format(res))
        doc = nlp(res)
        sents = list(doc.sents)
        for i in range(len(sents)):
            #print("sent: {}".format(sents[i]))
            if '?' in sents[i].text and \
               i+1 < len(sents):
                next_sent = sents[i+1]
                print("Next sent: {}".format(next_sent.text))
                #print("Length of the next sent: {}".format(len(next_sent)))                

                is_valid = False
                begin_idx = next_sent[0].i
                for token in next_sent:
                    tk_idx = token.i

                    #print("Token: {}, IS_NUM: {}, POS: {}, IDX: {}".format(token.text, token.pos == NUM, token.pos, tk_idx))
                    if token.pos == NUM and (tk_idx - begin_idx) < len(next_sent) - 1:
                        next_idx = tk_idx + 1
                        next_token = doc[next_idx]
                        next_token_text = next_token.text
                        print("Next token text: {}".format(next_token_text))
                        if "dollar" in next_token_text or \
                           "yen" in next_token_text or \
                           "euro" in next_token_text or \
                           "yuan" in next_token_text or \
                           "$" in next_token_text or \
                           "USD" in next_token_text or \
                           "€" in next_token_text:
                            is_valid = True
                            break

                if not is_valid:
                    break
                
                ins_count += 1
                output_file.write(next_sent.text + "\n")
                break

    return ins_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ifname", type=str, help="The input file", default="")
    parser.add_argument("-ofname", type=str, help="The output file", default="")
    parser.add_argument("-verbose", type=int, help="Indicate whether the questions should be output.", default=0)        
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()

    ifname = args.ifname
    ofname = args.ofname
    verbose = args.verbose
    pad_right = args.padding_right
    ins_count = 0
    with open(ofname, "w") as ofile:
        with open(ifname, "r", errors='replace') as ifile:
            doc = ifile.read()
            ins_count += extract_sents(doc, ofile, verbose, pad_right)
            
    print("Number of total entries: {}".format(ins_count))
