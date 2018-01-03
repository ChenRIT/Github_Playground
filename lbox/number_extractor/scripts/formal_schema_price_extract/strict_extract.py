# Extract sentences containing "$"+Arabic numerals from ClueWeb contents
# The format of labels conforms to the formal schema

# The purpose of this script is to:
# 1. Get basic training data.
# 2. Show the challenge of rule-based extraction.

import re
import argparse
import spacy

nlp = spacy.load('en_core_web_sm')

# reg_res -> ordered matches -> result parsing

def clean_res1(search_res):
    '''
    Clean the result returned by regular expression matching

    Arguments:
    search_res -- (inequality_indicator, dollar_sign, dollar_sign_amount, dollar_text_amount, dollar_text, unit)

    Return:
    a five-element tuple: (inequality_indicator, lower_number, upper_number, currency_unit, rate_unit)
    '''

    ineq_indi = search_res[0]
    rate_unit = None
    upper_number = None
    
    if search_res[1]:
        lower_number = search_res[2]
        currency_unit = 'dollar'
    elif search_res[4] is None:
        print("No currency detected!")
        return None
    else:
        lower_number = search_res[3]
        currency_unit = 'dollar'

    return (ineq_indi, lower_number, upper_number, currency_unit, rate_unit)

    
def parse_res(ordered_res):
    ''' 
    Parse the matching results of regular expressions.

    Arguments:
    ordered_res -- a five-element tuple: (inequality_indicator, lower_number, upper_number, currency_unit, rate_unit)

    Return: 
    a six-element tuple: (lower bound, left closeness, upper bound, right closeness, unit, rate unit)
    '''

    left_bound = ordered_res[1]
    left_closeness = 0
    right_bound = ordered_res[2]
    right_closeness = 0
    unit = ordered_res[3]
    rate_unit = ordered_res[4]
    
    if not left_bound:
        # No number found
        print("No number found!")
        return None

    if right_bound:
        # Upper number exists
        return (left_bound, 1, right_bound, 1, unit, rate_unit)

    # with lower_number but no upper_number
    if not ordered_res[0]:
        # No range
        return (left_bound, 1, left_bound, 1, unit, rate_unit)

    if ordered_res[0] == 'more than' or ordered_res[0] == 'over':
        left_closeness = 0
        right_bound = float('inf')
        right_closeness = 0
        
    if ordered_res[0] == 'at least':
        left_closeness = 1
        right_bound = float('inf')
        right_closeness = 0
        
    if ordered_res[0] == 'less than':
        right_bound = left_bound
        right_closeness = 0        
        left_bound = float('-inf')
        left_closeness = 0

    return (left_bound, left_closeness, right_bound, right_closeness, unit, rate_unit)

def extract_dollarsign(input_texts, output_file, pre_pad_num=100, post_pad_num=100):
    """ Extract the sentences containing price values

    @return: the number of instances found
    """

    ins_count = 0
    # reg_exp = "(.{" + str(pre_pad_num) + "}" + "((?:no more than)|(?:more than)|(?:at least)|(?:over)|(?:less than))?" + "\s?" + \
    #           "(\$)?" + "\s?" + "([0-9.,]+[0-9])" + "\s?" + "((?:dollar(?:s))|(?:euro(?:s))|(?:yen(?:s))|(?:yuan(?:s)))?" + \
    #           "(per \w+)?" + ".{" + str(post_pad_num) + "})"
    #reg_exp = "(.{" + str(pre_pad_num) + "}" + "(\\$)?" + "([0-9.,]+[0-9])" + "\\s?" + "(dollar)" + ".{" + str(post_pad_num) + "})"

    # Example: $300 or 300 dollars
    # reg_exp = "(.{" + str(pre_pad_num) + "}" + "(?:(\\$)([0-9.,]+[0-9])" + "|" + "(?:([0-9.,]+[0-9])(?:\\s)(dollar)))" + ".{" + str(post_pad_num) + "})"

    # Example:  more than $300/300 dollars
    reg_exp = "(.{" + str(pre_pad_num) + "}" + "((?:more than)|(?:less than)|(?:over)|(?:at least))?" + "(?:\\s)?" + "(?:(\\$)([0-9.,]+[0-9])" + "|" + \
              "(?:([0-9.,]+[0-9])(?:\\s)(dollar)))" + ".{" + str(post_pad_num) + "})"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.S)
    print("Found {} instances.".format(len(results)))

    for res in results:
        origin_string = res[0]

        if res[3]:
            numerals = res[3]
        else:
            numerals = res[4]
        
        doc = nlp(origin_string)
        for sent in doc.sents:
            if numerals in sent.text:
                if "\n\n\n" not in sent.text and "=" not in sent.text:
                    search_res = re.search("price", sent.text, re.I)
                    if search_res:
                        ins_count += 1
                        
                        origin_text = sent.text
                        #print("Match result: {}".format(res))                        
                        ordered_res = clean_res1(res[1:])                        
                        label = parse_res(ordered_res)
                        #print("label: {}".format(label))
                        data_entry = (sent.text, label)
                        output_file.write(str(data_entry) + "\n")
                break

    return ins_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-pl", "--padding_left", type=int, help="The number of characters to be extracted to the left of the searched pattern", default=100)
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()
    
    input_file = "../../data/00_warc_contents.txt"
    output_fname = "./number_extract_results.txt"
    pad_left = args.padding_left
    pad_right = args.padding_right
    ins_count = 0
    with open(output_fname, "w+") as ofile:
        with open(input_file, "r", errors='replace') as ifile:
            doc = ifile.read()
            ins_count += extract_dollarsign(doc, ofile, pad_left, pad_right)

    print("Number of entries: {}".format(ins_count))
