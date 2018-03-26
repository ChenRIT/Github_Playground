import sys
import csv
import re
import argparse

import spacy
from spacy.symbols import NUM

nlp = spacy.load('en')

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-ifname", type=str, help="The input text file", default="training_10000.txt")
    args = parser.parse_args()
  
    input_fname = args.ifname
    sents = []    
    with open(input_fname) as ifile:
        for line in ifile:
            new_line = separate_numbers(line)
            sents.append(new_line)
    # print("sents: {}".format(sents))

    # Read extraction rules for labeling
    # extract_fname = "./exp_patterns_label.csv"
    extract_fname = "./exp_pattern_100.csv"    
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
    output_fname = "./label_data.csv"
    output_num = 0
    with open(output_fname, 'w') as ofile:
        sentwriter = csv.writer(ofile)
        sentwriter.writerow(['index', 'sentence', 'label'])
        label_data = []
        label_idx = 0
        for sent_tuple in abs_sents:
            ori_sent, conv_sent, mapping = sent_tuple
            print("original sent: {}".format(ori_sent))
            print("converted sent: {}".format(conv_sent))
            print("mapping: {}".format(mapping))

            # Apply the rule which has the longest pattern
            rule_match = False
            match_rules = []
            for i in range(len(ext_rules)):
                rule = ext_rules[i]
                pattern = rule[0]
                extract = rule[1]
                search_pattern = pattern
                # Pre-process patterns
                for i in range(10):
                    str_to_repl = '_' + str(i)
                    search_pattern = search_pattern.replace(str_to_repl, "_[0-9]")
                search_pattern = search_pattern.replace(")", "\)")
                search_pattern = search_pattern.replace("$", "\$")                
                # print("Search pattern: {}".format(search_pattern))
                search_res = re.search(search_pattern, conv_sent)
                if search_res:
                    match_rules.append(rule)
                    rule_match = True

            if not rule_match:
                print("No rule match for sent: {}".format(ori_sent))
                sentwriter.writerow([label_idx, ori_sent, "(-|-|-|-|-)"])
                output_num += 1
                label_idx += 1
                continue

            # Use candidate rules for extraction. Start from the longest rule
            sorted_rules = sorted(match_rules, key=lambda pair: len(pair[0]), reverse=True)
            #print("Candidate rules: {}".format(sorted_rules))
            rule_idx = 0
            sent_to_search = conv_sent
            is_match = False
            extract_values = ""
            while rule_idx < len(sorted_rules):
                rule_cand = sorted_rules[rule_idx]
                pattern_ext = rule_cand[0]
                extract_ext = rule_cand[1]
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
                    rule_idx += 1
                    continue

                #print("Matched pattern: {}".format(search_pattern))
                is_match = True
                first_num = match_res.group(1)
                digit = first_num[-1:]
                #print("Digit: {}".format(digit))
                diff = int(digit) - 1
                mod_extract = extract_ext
                for i in reversed(range(10)):
                    str_to_repl = 'NUM_' + str(i)
                    num_repl = i+diff
                    #print("Num replace: {}".format(num_repl))
                    mod_extract = mod_extract.replace(str_to_repl, "NUM_"+str(num_repl))
                #print("Template extraction: {}".format(mod_extract))
                
                # Use the rule to extract the value
                for sym, val in mapping.items():
                    if sym in mod_extract:
                        mod_extract = mod_extract.replace(sym, val)

                # Use the token after "per" as rate unit
                sent_nlp = nlp(ori_sent)
                contain_per = False
                for token in sent_nlp:
                    if contain_per:
                        unit = token.text
                        mod_extract = mod_extract.replace("-)", unit+")")
                        break
                    if token.text == "per":
                        contain_per = True
                        
                if extract_values == "":
                    extract_values = mod_extract
                else:
                    extract_values += ":" + mod_extract

                # Remove the matched part
                sent_to_search = sent_to_search.replace(match_res.group(0), "")
                # print("Modified sent: {}".format(sent_to_search))
                rule_idx = 0

            if not is_match:
                print("No match found!")
                extract_values = "(-|-|-|-|-)"
                
            sentwriter.writerow([label_idx, ori_sent, extract_values])
            output_num += 1
            label_idx += 1

    print("Total sentences output: {}".format(output_num))
            
