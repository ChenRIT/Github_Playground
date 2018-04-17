import sys
import csv
import re
import argparse

import spacy
from spacy.symbols import NUM

nlp = spacy.load('en_core_web_lg')

def separate_numbers(sent):
  # Separate numbers and its following words, e.g., 6.99you
  for m in re.findall("(\D*)(\d?[0-9\,\.]*\d)(\D*)", sent):
    m = [x for x in m if x]
    sent = sent.replace(''.join(m), ' ' + ' '.join(m) + ' ')
    sent = ' '.join(sent.split())
  return sent

def abstract_number(sent_string):
    num_idx = 1
    num_to_val = {}
    sent_parse = nlp(sent_string)
    ori_sent = ""
    new_sent = ""
    is_num_chunk = False
    num_chunks = ""

    ori_sent = sent_string
    
    for token in sent_parse:
        #print("Pos of {} is {}".format(token.text, token.pos_))
        if token.pos == NUM:
            #print("Number: {}".format(token.text))
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-ifname", type=str, help="The input text file", default="training_10000.txt")
    parser.add_argument("-lfname", type=str, help="The csv file used for labeling", default="label.csv")
    parser.add_argument("-ofname", type=str, help="The output file", default="label_data.csv")        
    args = parser.parse_args()

    print("Required labeling schema: (index, pattern, lb, ub, currency, rate)")
    
    input_fname = args.ifname
    sents = []    
    with open(input_fname) as ifile:
        for line in ifile:
            doc = nlp(line)
            new_line = separate_numbers(doc.text)
            sents.append(new_line)

    # Read extraction rules for labeling
    # extract_fname = "./exp_patterns_label.csv"
    extract_fname = args.lfname
    ext_rules = []
    with open(extract_fname) as pfile:
        ext_csv = csv.reader(pfile)
        for row in ext_csv:
            ext_rules.append(row)
    ext_rules = ext_rules[1:] # The first row is the schema
    # print("extraction_rules: {}".format(ext_rules))            

    # Convert all number chunks in the input sentences into NUM, and append an index to each NUM.
    # Keep the mapping between each NUM and the original number chunks.
    abs_sents = []
    for sent in sents:
        convert_sent = abstract_number(sent)
        abs_sents.append(convert_sent)
    print("Number of sents: {}".format(len(abs_sents)))        
        
    # Use patterns to match against the sentence, and return the extraction results of the first matched pattern.
    output_fname = args.ofname
    output_num = 0
    with open(output_fname, 'w') as ofile:
        sentwriter = csv.writer(ofile)
        sentwriter.writerow(['index', 'sentence', 'lb', 'ub', 'currency', 'rate'])
        label_data = []
        label_idx = 0
        sorted_rules = sorted(ext_rules, key=lambda tp: len(tp[1]), reverse=True)        
        for sent_tuple in abs_sents:
            ori_sent, conv_sent, mapping = sent_tuple
            # print("original sent: {}".format(ori_sent))
            # print("converted sent: {}".format(conv_sent))
            # print("mapping: {}".format(mapping))

            # Use candidate rules for extraction. Start from the longest rule
            sent_to_search = conv_sent
            is_match = False
            extract_values = []
            for rule_cand in sorted_rules:
                pattern_ext = rule_cand[1]
                extract_ext = rule_cand[2:]
                search_pattern = pattern_ext
                # Pre-process patterns
                search_pattern = search_pattern.replace(")", "\)")
                search_pattern = search_pattern.replace("$", "\$")
                #print("Match pattern: {}".format(search_pattern))                
                for i in range(10):
                    str_to_repl = 'NUM_' + str(i)
                    search_pattern = search_pattern.replace(str_to_repl, "(NUM_.)")

                # Match the pattern
                #print("Revised pattern: {}".format(search_pattern))                
                match_res = re.search(search_pattern, sent_to_search)
                if match_res is None:
                    continue

                #print("Matched pattern: {}".format(search_pattern))
                is_match = True
                first_num = match_res.group(1)
                digit = first_num[-1:]
                #print("Digit: {}".format(digit))
                diff = int(digit) - 1
                mod_extract = []
                for ext in extract_ext:
                    new_ext = ext
                    for i in reversed(range(10)):
                        str_to_repl = 'NUM_' + str(i)
                        num_repl = i+diff
                        new_ext = new_ext.replace(str_to_repl, "NUM_"+str(num_repl))
                    mod_extract.append(new_ext)
                print("Mod_extract: {}".format(mod_extract))
                
                # Use the rule to extract the value
                print("mapping: {}".format(mapping))
                repl_extract = []
                for ext in mod_extract:
                    new_ext = ext
                    for sym, val in mapping.items():
                        if sym in ext:
                            new_ext = ext.replace(sym, val)
                    repl_extract.append(new_ext)
                print("Repl_extract: {}".format(repl_extract))

                # Use the token after "per" as rate unit
                final_extract = repl_extract[:-1]
                sent_nlp = nlp(ori_sent)
                contain_per = False
                for token in sent_nlp:
                    if contain_per:
                        unit = token.text
                        final_extract.append(unit)
                        break
                    if token.text == "per":
                        contain_per = True
                        
                if not contain_per:
                  final_extract.append("-")

                print("Final_extract: {}".format(final_extract))

                break
                # End of rule searching
                        
            if not is_match:
                print("No match for sents: {}".format(ori_sent))
                print("Converted sents: {}".format(conv_sent))                
                final_extract = ["-", "-", "-", "-"]
                
            sentwriter.writerow([label_idx, ori_sent] + final_extract)
            output_num += 1
            label_idx += 1

    print("Total sentences output: {}".format(output_num))
            
