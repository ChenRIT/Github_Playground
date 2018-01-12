# Extract sentences containing "$"+Arabic numerals from ClueWeb contents

import re
import argparse
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_dollarsign(input_texts, output_file, pre_pad_num=100, post_pad_num=100):
    """ Extract the sentences containing "$"+Arabic numberals

    @return: the number of instances found
    """

    ins_count = 0
    reg_exp = "(.{" + str(pre_pad_num) + "}(\$[0-9.,]+[0-9]).{" + str(post_pad_num) + "})"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.S)

    for res in results:
        doc = nlp(res[0])
        for sent in doc.sents:
            if res[1] in sent.text:
                if "\n\n\n" not in sent.text and "=" not in sent.text:
                    search_res = re.search("price", sent.text, re.I)
                    if search_res:
                        ins_count += 1
                        data_entry = (sent.text, res[1])
                        output_file.write(str(data_entry) + "\n")
                break

    return ins_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-pl", "--padding_left", type=int, help="The number of characters to be extracted to the left of the searched pattern", default=100)
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()
    
    input_file = "../data/00_warc_contents.txt"
    output_fname = "./number_extract_results.txt"
    pad_left = args.padding_left
    pad_right = args.padding_right
    ins_count = 0
    with open(output_fname, "w+") as ofile:
        with open(input_file, "r", errors='replace') as ifile:
            doc = ifile.read()
            ins_count += extract_dollarsign(doc, ofile, pad_left, pad_right)

    print("Number of entries: {}".format(ins_count))
