# Replace all number chunks in the document with a special symbol __NUM__

import argparse

import spacy
from spacy.symbols import NUM

nlp = spacy.load('en')

def abstract_number(sent_string):
    sent_parse = nlp(sent_string)
    new_sent = ""
    is_num_chunk = False
    for token in sent_parse:
        if token.pos == NUM:
            if is_num_chunk:
                continue
            else:
                is_num_chunk = True
        else:                    
            if is_num_chunk:
                new_sent += "NUM "
                is_num_chunk = False
                new_sent += token.text + " " 
    return new_sent
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-attr", type=str, help="The attribute considered.", default="price")    
    args = parser.parse_args()

    attr = args.attr
    ifname = attr + "_results.txt"
    ofname = attr + "_results_num.txt"
    with open(ifname) as ifile:
        with open(ofname, "w") as ofile:
            doc = nlp(ifile.read())
            new_doc = ""
            is_num_chunk = False
            for token in doc:
                if token.pos == NUM:
                    if is_num_chunk:
                        continue
                    else:
                        is_num_chunk = True
                else:                    
                    if is_num_chunk:
                        new_doc += "NUM "
                        is_num_chunk = False
                    new_doc += token.text + " " 
            ofile.write(new_doc)
