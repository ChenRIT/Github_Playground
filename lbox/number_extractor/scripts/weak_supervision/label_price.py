import sys
import csv

import spacy
from spacy.symbols import NUM

nlp = spacy.load('en')

def abstract_number(sent_string):
    num_idx = 1
    num_to_val = {}
    sent_parse = nlp(sent_string)
    ori_sent = ""
    new_sent = ""
    is_num_chunk = False
    num_chunks = ""

    for token in sent_parse:
        ori_sent += token.text + " "
    
    for token in sent_parse:
        if token.pos == NUM:
            if is_num_chunk:
                num_chunks = num_chunks + " " + token.text                            
            else:
                num_chunks = token.text                                            
                is_num_chunk = True
        else:                    
            if is_num_chunk:
                num_id = "NUM_" + str(num_idx)
                new_sent += num_id + " "
                new_sent += token.text + " "
                
                is_num_chunk = False
                num_to_val[num_id] = num_chunks
                num_chunks = ""
                num_idx += 1
            else:
                new_sent += token.text + " "

    # Handle the case when the number chunk is at the end of the sentences.         
    if is_num_chunk:
        num_id = "NUM_" + str(num_idx)
        new_sent += num_id + "."
        num_to_val[num_id] = num_chunks
        
    return (ori_sent, new_sent, num_to_val)

if __name__ == "__main__":
    # Read input sentences
    input_fname = "./exp_sentences.txt"
    sents = []    
    with open(input_fname) as ifile:
        for line in ifile:
            sents.append(line)
    # print("sents: {}".format(sents))

    # Read extraction rules for labeling
    extract_fname = "./exp_patterns_label.csv"
    ext_rules = []
    with open(extract_fname) as pfile:
        ext_csv = csv.reader(pfile)
        for row in ext_csv:
            ext_rules.append(row)
    # print("extraction_rules: {}".format(ext_rules))            

    # Convert all number chunks in the input sentences into NUM, and append an index to each NUM.
    # Keep the mapping between each NUM and the original number chunks.
    abs_sents = []
    for sent in sents:
        convert_sent = abstract_number(sent)
        abs_sents.append(convert_sent)
        
    # Use patterns to match against the sentence, and return the extraction results of the first matched pattern.
    output_fname = "./label_data.csv"
    with open(output_fname, 'w') as ofile:
        sentwriter = csv.writer(ofile)
        label_data = []
        for sent_tuple in abs_sents:
            ori_sent, conv_sent, mapping = sent_tuple
            print("original sent: {}".format(ori_sent))
            print("converted sent: {}".format(conv_sent))
            print("mapping: {}".format(mapping))

            # Apply the rule which has the longest pattern
            rule_match = False
            ext_rule_id = 0
            max_length = 0
            for i in range(len(ext_rules)):
                rule = ext_rules[i]
                pattern = rule[0]
                extract = rule[1]
                if pattern in conv_sent and len(pattern) > max_length:
                    max_length = len(pattern)
                    ext_rule_id = i
                    rule_match = True

            if not rule_match:
                print("No rule match for sent: {}".format(ori_sent))
                continue

            rule_for_ext = ext_rules[ext_rule_id]
            pattern_ext = rule_for_ext[0]
            extract_ext = rule_for_ext[1]
            print("Matched pattern: {}".format(pattern_ext))
            print("Template extraction: {}".format(extract_ext))
            # Use the rule to extract the value
            val_extract = extract_ext
            for sym, val in mapping.items(): 
                if sym not in val_extract:
                    print("No {} found".format(sym))
                    sys.exit()
                else:
                    val_extract = val_extract.replace(sym, val)
            sentwriter.writerow([ori_sent, val_extract])



