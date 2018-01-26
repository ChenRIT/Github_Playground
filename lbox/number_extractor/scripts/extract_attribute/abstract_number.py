# Replace all number chunks in the document with a special symbol __NUM__

import argparse

import spacy
from spacy.symbols import NUM

nlp = spacy.load('en')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ifname", type=str, help="The data file to be opened.", default="price_results.txt")
    parser.add_argument("-ofname", type=str, help="The output file to be opened.", default="price_results_num_symbol.txt")            
    args = parser.parse_args()

    ifname = args.ifname
    ofname = args.ofname
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
                        new_doc += " NUM "
                        is_num_chunk = False
                    new_doc += token.text + " " 
            ofile.write(new_doc)
