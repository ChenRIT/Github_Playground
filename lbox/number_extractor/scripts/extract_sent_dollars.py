# Extract sentences containing "dollar" from ClueWeb contents

import re
import argparse
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_dollar_amount(input_texts, output_file, attribute, unit, pre_pad_num=100, post_pad_num=100):
    """ Extract the sentences containing the "attribute" and "unit"

    @return: the number of instances found
    """

    ins_count = 0
    reg_exp = ".{" + str(pre_pad_num) + "}" + attribute + ".{" + str(post_pad_num) + "}"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.S)

    for res in results:
        doc = nlp(res)
        for sent in doc.sents:
            if unit in sent.text:
                ins_count += 1
                output_file.write(sent.text + "\n\n\n")

    return ins_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--attribute", type=str, help="The attribute that is of interest", default="price")
    parser.add_argument("-u", "--unit", type=str, help="The most popular unit of the interested attribute", default="dollar")    
    parser.add_argument("-pl", "--padding_left", type=int, help="The number of characters to be extracted to the left of the searched pattern", default=100)
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()
    
    input_file = "../data/00_warc_contents.txt"
    output_fname = "./number_extract_results.txt"
    attribute = args.attribute
    unit = args.unit
    pad_left = args.padding_left
    pad_right = args.padding_right
    ins_count = 0
    with open(output_fname, "w+") as ofile:
        with open(input_file, "r", errors='replace') as ifile:
            doc = ifile.read()
            ins_count += extract_dollar_amount(doc, ofile, attribute, unit, pad_left, pad_right)

    print("Number of entries: {}".format(ins_count))
