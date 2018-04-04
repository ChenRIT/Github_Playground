# Extract sentences containing "$"+Arabic numerals from ClueWeb contents

import re
import argparse
import spacy

nlp = spacy.load('en_core_web_sm')

currencies = [r'dollar', r'$', r'buck', r'yen', r'¥', r'euro', r'€', r'yuan']

def extract_dollarsign(input_texts, output_file, pre_pad_num=100, post_pad_num=100, maxlen=20):
    """ Extract the sentences containing "$"+Arabic numberals

    @return: the number of instances found
    """

    ins_count = 0
    reg_exp = ".{" + str(pre_pad_num) + "}(?:price)|(?:cost)|(?:charge).{" + str(post_pad_num) + "}"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.S)
    print("Find {} instances".format(len(results)))    
    for res in results:
        doc = nlp(res)
        for sent in doc.sents:
            plain_text = sent.text
            if ("price" in plain_text) or \
               ("cost" in plain_text) or \
               ("charge" in plain_text):

                plain_text = plain_text.rstrip()
                if plain_text[0].islower() or "   " in plain_text or "\n" in plain_text:
                    break

                if len(sent) < 2 or len(sent) > maxlen:
                    break

                has_currency = False
                for cur in currencies:
                    if cur in plain_text:
                        has_currency = True
                        break

                if not has_currency:
                    break
                
                has_num = False
                for token in sent:
                    if token.pos == spacy.symbols.NUM:
                        has_num = True
                        break

                if not has_num:
                    break

                ins_count += 1
                output_file.write(plain_text + "\n")
                break

    return ins_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ifname", type=str, help="The input file", default="")
    parser.add_argument("-ofname", type=str, help="The output file", default="")
    parser.add_argument("-maxlen", type=int, help="The maximum length of a sentence", default=20)        
    parser.add_argument("-pl", "--padding_left", type=int, help="The number of characters to be extracted to the left of the searched pattern", default=100)
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()
    
    input_file = args.ifname
    output_fname = args.ofname
    maxlen = args.maxlen
    pad_left = args.padding_left
    pad_right = args.padding_right
    ins_count = 0
    with open(output_fname, "w+") as ofile:
        with open(input_file, "r", errors='replace') as ifile:
            doc = ifile.read()
            ins_count += extract_dollarsign(doc, ofile, pad_left, pad_right, maxlen)

    print("Number of entries: {}".format(ins_count))
 
