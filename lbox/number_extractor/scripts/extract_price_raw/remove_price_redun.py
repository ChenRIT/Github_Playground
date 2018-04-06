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
    input_file = "./test_redundant_sents.txt"
    output_file = "./test_redun_removed.txt"

    template_pool = []
    non_redun_sents = []
    with open(input_file) as ifile:
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
