# Extract sentences containing "$"+Arabic numerals from ClueWeb contents

from os import listdir
from os.path import isfile, join

import re
import argparse
import spacy
from spacy.symbols import NUM

nlp = spacy.load('en_core_web_sm')

#questions = ['(?:how much does it cost)', '(?:what is the price)']

def extract_sents(input_texts, output_file, keyword, units, post_pad_num=100):
    """ Extract the sentences containing question answer pairs

    @return: the number of instances found
    """

    ins_count = 0
    #reg_exp = "(?:" + '|'.join(questions) + ")" + ".{" + str(post_pad_num) + "}"
    reg_exp = keyword + r".{,20}\?.{" + str(post_pad_num) + "}"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.S|re.I)
    print("Find {} instances".format(len(results)))

    # for res in results:
    #     print(res)

    for res in results:
        doc = nlp(res)
        sents = list(doc.sents)
        for i in range(len(sents)):
            if keyword in sents[i].text and \
               '?' in sents[i].text and \
               i+1 < len(sents):
                next_sent = sents[i+1]
                #search_num = re.search(r"[0-9.,]+[0-9]", next_sent.text)
                # if search_num:

                has_unit = False
                has_num = False                
                for token in next_sent:
                    if token.pos == NUM:
                        has_num = True
                        if has_unit and has_num:
                            break

                    if token.text in units:
                        has_unit = True
                        if has_unit and has_num:
                            break
                        
                if not has_num or not has_unit:
                    continue
                    
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
    parser.add_argument("-keyword", type=str, help="The keyword to be searched in the question", default='cost')
    parser.add_argument("-units", nargs='+', help="The units to be searched for.", default="dollar")    
    parser.add_argument("-dir", type=str, help="The directory to find input files.", default=None)    
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()

    ifnames = args.ifnames
    keyword = args.keyword    
    ofname = keyword + "_results.txt"
    units = args.units
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
                    ins_count += extract_sents(doc, ofile, keyword, units, pad_right)
            
    #print("Number of final entries: {}".format(ins_count))
