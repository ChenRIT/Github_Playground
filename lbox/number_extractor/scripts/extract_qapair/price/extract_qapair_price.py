# Extract sentences following a question seeded by the attribute

from os import listdir
from os.path import isfile, join

import re
import argparse
import spacy
from spacy.symbols import NUM

nlp = spacy.load('en_core_web_sm')

#questions = ['(?:how much does it cost)', '(?:what is the price)']

def extract_sents(input_texts, output_file, q_kw, a_kw, has_num, verbose, post_pad_num=100):
    """ Extract the sentences containing question answer pairs

    @return: the number of instances found
    """

    ins_count = 0
    #reg_exp = "(?:" + '|'.join(questions) + ")" + ".{" + str(post_pad_num) + "}"
    reg_exp = q_kw + r".{,20}\?.{" + str(post_pad_num) + "}"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.S|re.I)
    print("Find {} instances".format(len(results)))

    if verbose:
        for res in results:
            print(res)

    for res in results:
        #print("Matched sent: {}".format(res))
        doc = nlp(res)
        sents = list(doc.sents)
        for i in range(len(sents)):
            qkw_res = re.search(q_kw, sents[i].text, re.I)
            if qkw_res and \
               '?' in sents[i].text and \
               i+1 < len(sents):
                next_sent = sents[i+1]
                #print("Next sent: {}".format(next_sent))
                #search_num = re.search(r"[0-9.,]+[0-9]", next_sent.text)
                # if search_num:

                if a_kw:
                    has_kw = False
                else:
                    has_kw = True

                if has_num:
                    num_exist = False
                else:
                    num_exist = True
                    
                for token in next_sent:
                    if has_num and token.pos == NUM:
                        num_exist = True
                        if has_kw and num_exist:
                            break

                    if a_kw is not None:
                        for kw in a_kw:
                            token_res = re.search(kw, token.text, re.I)
                            if token_res:
                                has_kw = True
                                break
                            
                        if has_kw and num_exist:
                            break
                        
                if not num_exist or not has_kw:
                    break
                    
                ins_count += 1
                # print("Question: " + sents[i].text + "\n")
                # print("Answer: " + next_sent.text + "\n\n")                    
                # output_file.write("Question: " + sents[i] + "\n")
                output_file.write(next_sent.text + "\n")
                break

    return ins_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ifnames", nargs='+', help="The data files to be opened.", default=None)
    parser.add_argument("-dir", type=str, help="The directory to find input files.", default=None)        
    parser.add_argument("-qk", type=str, help="The keyword to be searched for in the question", default=None)
    parser.add_argument("-ak", nargs='+', help="The keywords to be searched for in the answer.", default=None)
    parser.add_argument("-has_num", type=int, help="Indicate whether the answer should contain a number.", default=0)
    parser.add_argument("-verbose", type=int, help="Indicate whether the questions should be output.", default=0)        
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()

    ifnames = args.ifnames
    q_kw = args.qk
    a_kw = args.ak
    has_num = args.has_num
    verbose = args.verbose
    ofname = q_kw + "_results.txt"
    dir = args.dir
    pad_right = args.padding_right
    ins_count = 0
    all_files = []
    with open(ofname, "w") as ofile:
        if ifnames:
            all_files += ifnames

        if dir:
            dir_files = [join(dir,f) for f in listdir(dir) if isfile(join(dir, f))]
            all_files += dir_files

        for fname in all_files:
            if "warc.gz.txt" in fname:
                with open(fname, "r", errors='replace') as ifile:
                    doc = ifile.read()
                    ins_count += extract_sents(doc, ofile, q_kw, a_kw, has_num, verbose, pad_right)
            
    print("Number of total entries: {}".format(ins_count))
