# Process ClueWeb with regular expression

import re
import argparse


def extract_numbers(input_texts, output_file, pattern="", pre_pad_num=10, post_pad_num=100):
    """ Extract pattern from warc_fname and output to output_file handler.

    @return: the number of instances found
    """

    ins_count = 0
    search_pattern = pattern
    reg_exp = ".{" + str(pre_pad_num) + "}" + search_pattern + ".{" + str(post_pad_num) + "}"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.S)
    ins_count += len(results)
    for res in results:
        output_file.write(res + "\n\n\n")

    return ins_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", type=str, help="The pattern to be searched for", default="")
    parser.add_argument("-pl", "--padding_left", type=int, help="The number of characters to be extracted to the left of the searched pattern", default=100)
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()
    
    input_file = "../data/00_warc_contents.txt"
    output_fname = "./number_extract_results.txt"
    search_pattern = args.pattern
    pad_left = args.padding_left
    pad_right = args.padding_right
    with open(output_fname, "w+") as ofile:
        with open(input_file, "r") as ifile:
            doc = ifile.read()
            extract_numbers(doc, ofile, search_pattern, pad_left, pad_right)
