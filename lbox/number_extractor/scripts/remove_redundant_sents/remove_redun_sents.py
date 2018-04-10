import os
import argparse
import spacy

nlp = spacy.load('en_core_web_sm')

def get_template(sent):
    doc = nlp(sent)
    new_sent = ""
    for token in doc:
        if token.pos == spacy.symbols.NUM:
            new_sent += "NUM "
        else:
            new_sent += token.text + " "
    return new_sent

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-idir", type=str, help="The input directory", default=".")
    parser.add_argument("-ofname", type=str, help="The name of the output file", default="./no_redun_sents.txt")
    args = parser.parse_args()
    
    input_dir = args.idir
    output_file = args.ofname

    template_pool = []
    non_redun_sents = []
    for fname in os.listdir(input_dir):
        if fname.endswith(".warc.gz.txt"):
            fpath = os.path.join(input_dir, fname)
            with open(fpath) as ifile:
                for line in ifile:
                    sent_template = get_template(line)
                    if sent_template in template_pool:
                        continue
                    else:
                        template_pool.append(sent_template)
                        non_redun_sents.append(line)

    with open(output_file, "w") as ofile:
        for sent in non_redun_sents:
            ofile.write(sent)
