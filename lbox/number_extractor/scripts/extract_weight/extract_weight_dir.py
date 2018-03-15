# Extract sentences containing "$"+Arabic numerals from ClueWeb contents

from os import listdir
from os.path import isfile, isdir, join

import re
import argparse

import spacy
from spacy.symbols import NUM, SPACE

nlp = spacy.load('en_core_web_sm')

def search_sents(dir, ofile, pad_left, pad_right):
    """
    Search for all sentences that match the search condition.
    """
    ins_count = 0
    for f in listdir(dir):
        file_path = join(dir, f)
        if isfile(file_path) and "warc.gz.txt" in f:
            with open(file_path, "r", errors='replace') as ifile:
                doc = ifile.read()
                ins_count += extract_weight(doc, ofile, pad_left, pad_right)
        elif isdir(file_path):
            ins_count += search_sents(file_path, ofile, pad_left, pad_right)

    return ins_count

def remove_space(doc):
    new_sent = ""
    for token in doc:
        if token.pos != SPACE:
            new_sent += token.text + " "

    return new_sent[:-1]

def extract_weight(input_texts, output_file, pre_pad_num=100, post_pad_num=100):
    """ Extract the sentences containing "weight" and at least one number

    @return: the number of instances found
    """

    ins_count = 0
    reg_exp = ".{" + str(pre_pad_num) + "}(?: kg)|(?: lb)|(?: kilogram)|(?: gram)|(?: pound)|(?: ounce)|(?: tons).{" + str(post_pad_num) + "}"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.S|re.I)
    print("Find {} instances".format(len(results)))

    for res in results:
        doc = nlp(res)
        for sent in doc.sents:
            # search_weight = re.search(r"weight", sent.text, re.I)
            # if search_weight is None:
            #     continue

            sent_text = sent.text
            if " kg" not in sent_text and \
               " lb" not in sent_text and \
               " kilogram" not in sent_text and \
               " gram" not in sent_text and \
               " pound" not in sent_text and \
               " ounce" not in sent_text and \
               " tons" not in sent_text:
                continue

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
    parser.add_argument("-dir", type=str, help="The directory where ClueWeb files exist", default=".")
    parser.add_argument("-pl", "--padding_left", type=int, help="The number of characters to be extracted to the left of the searched pattern", default=100)
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()
    
    input_dir = args.dir
    output_fname = "./weight_extract_results.txt"
    pad_left = args.padding_left
    pad_right = args.padding_right
    ins_count = 0

    with open(output_fname, "w+") as ofile:
        ins_count += search_sents(input_dir, ofile, pad_left, pad_right)

    print("Number of entries: {}".format(ins_count))
