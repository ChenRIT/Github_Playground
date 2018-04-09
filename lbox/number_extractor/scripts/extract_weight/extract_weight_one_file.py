# Extract sentences containing weight units from ClueWeb

import re
import argparse

import spacy
from spacy.symbols import NUM, SPACE

nlp = spacy.load('en_core_web_sm')

def remove_space(doc):
    new_sent = ""
    for token in doc:
        if token.pos != SPACE:
            new_sent += token.text + " "

    return new_sent[:-1]

def extract_dollarsign(input_texts, output_file, pre_pad_num=100, post_pad_num=100):
    """ Extract the sentences containing "weight" and at least one number

    @return: the number of instances found
    """

    ins_count = 0
    reg_exp = ".{" + str(pre_pad_num) + "}weight.{" + str(post_pad_num) + "}"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.S|re.I)
    print("Find {} instances".format(len(results)))

    for res in results:
        doc = nlp(res)
        for sent in doc.sents:
            search_weight = re.search(r"weight", sent.text, re.I)
            if search_weight is None:
                continue
            
            search_unit = re.search(r"(?: kg )|(?: lbs)|(?: kilogram)|(?: pound)", sent.text, re.I)
            if search_unit is None:
                break

            has_num = False            
            for token in sent:
                if token.pos == NUM:
                    has_num = True
                    break

            if has_num:
                ins_count += 1
                new_sent = remove_space(sent)
                output_file.write(new_sent + "\n")
                break

    return ins_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-pl", "--padding_left", type=int, help="The number of characters to be extracted to the left of the searched pattern", default=100)
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()
    
    input_file = "../../data/clueweb/00.warc.gz.txt"
    output_fname = "./weight_extract_results.txt"
    pad_left = args.padding_left
    pad_right = args.padding_right
    ins_count = 0
    with open(output_fname, "w+") as ofile:
        with open(input_file, "r", errors='replace') as ifile:
            doc = ifile.read()
            ins_count += extract_dollarsign(doc, ofile, pad_left, pad_right)

    print("Number of entries: {}".format(ins_count))
