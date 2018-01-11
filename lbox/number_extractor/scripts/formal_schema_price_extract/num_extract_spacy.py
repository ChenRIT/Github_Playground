# Extract sentences containing prices
# The format of labels conforms to the formal schema

# The purpose of this script is to:
# 1. Get basic training data.
# 2. Show the challenge of rule-based extraction.

import re
import argparse
import spacy

nlp = spacy.load('en_core_web_sm')

# reg_res -> ordered matches -> result parsing


def extract_modifiers(input_text, number):
    '''
    Extract modifiers, such as unit or inequality

    '''
    lower_number = number
    lower_closeness = 1
    upper_number = number
    upper_closeness = 1
    currency = None
    rate_unit = None

    if 'more than' in input_text or \
       'over' in input_text:
        lower_closeness = 0
        upper_number = float('inf')
        upper_closeness = 0

    if 'less than' in input_text:
        lower_number = float('-inf')
        lower_closeness = 0
        upper_closeness = 0

    if 'at least' in input_text:
        upper_number = float('inf')
        upper_closeness = 0

    if 'dollar' in input_text or \
       '$' in input_text:
        currency = 'dollar'

    match_rate = re.search(r'per (\w+)', input_text)
    if match_rate:
        rate_unit = match_rate.group(1)

    return (lower_number, lower_closeness, upper_number, upper_closeness, currency, rate_unit)

def extract_num(sent):
    '''
    Extract the first digital number from the given text

    '''
    match_num = re.search(r'[0-9.,]+[0-9]', sent)
    if match_num:
        return match_num.group()
    else:
        return None

def extract_price(input_texts, output_file, pre_pad_num, post_pad_num):
    """ Extract the sentences containing price values

    @return: the number of instances found
    """

    ins_count = 0

    # Find all sentences containing "price"
    reg_exp = ".{" + str(pre_pad_num) + "}" + "price" +  ".{" + str(post_pad_num) + "}"
    results = re.findall(reg_exp, input_texts, re.S|re.I)
    print("Found {} instances.".format(len(results)))

    for res in results:
        print("=", end='')
        #print("res: {} of length {}".format(res, len(res)))
        doc = nlp(res)
        # Sift out the sentences containing 'price' and a number        
        for sent in doc.sents:
            #print("sent: {}".format(sent.text))
            match_obj = re.search(r'price', sent.text, re.I)
            if match_obj is None:
                #print("No price found!")
                continue

            # Extract number
            numbers = extract_num(match_obj.string)
 
            data_entry = (sent.text, label)
            ins_count += 1
            output_file.write(str(data_entry) + "\n")
            break

    return ins_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-pl", "--padding_left", type=int, help="The number of characters to be extracted to the left of the searched pattern", default=50)
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=50)
    args = parser.parse_args()
    
    input_file = "../../data/00_warc_contents.txt"
    #input_file = "./test_doc.txt"    
    output_fname = "./number_extract_results.txt"
    pad_left = args.padding_left
    pad_right = args.padding_right
    ins_count = 0
    with open(output_fname, "w+") as ofile:
        with open(input_file, "r", errors='replace') as ifile:
            doc = ifile.read()
            ins_count += extract_price(doc, ofile, pad_left, pad_right)

    print("Number of entries: {}".format(ins_count))
