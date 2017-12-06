# Input: a directory name
# Output: a file containing all lines of name introduction

import os
import argparse
from warc_proc_v3 import extract_names_warc

def extract_names_warc_dir(dir, output_file):
    """ Extract phrases that introduce names from all warc files under dir"""
    warc_ext = '.warc.gz'
    cur_dir = dir
    all_fnames = os.listdir(dir)
    
    for fname in all_fnames:
        file_path = os.path.join(cur_dir, fname)
        if os.path.isdir(file_path):
            # Handle subdirectories
            extract_names_warc_dir(file_path, output_file)

        if os.path.isfile(file_path):
            # Handle files
            if fname.endswith(warc_ext):
                # Process warc files
                extract_names_warc(file_path, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", type=str, help="The directory to be searched", default=".")
    parser.add_argument("-o", "--output", type=str, help="The name of the output file", default="name_patterns.txt")
    args = parser.parse_args()

    # Parse all .warc.gz files in the directory
    cur_dir = args.dir
    output_fname = args.output
    with open(output_fname, "a+") as ofile:        
        extract_names_warc_dir(cur_dir, ofile)
