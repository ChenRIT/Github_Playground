# Input: an input directory
# Output: Bash commands that extract weight sentences from all warc files in the input directory

import os
import sys
import argparse

def generate_weight_cmds(idir, odir):
    warc_ext = ".warc.gz.txt"
    all_fnames = os.listdir(idir)

    for fname in all_fnames:
        input_fpath = os.path.join(idir, fname)
        if os.path.isdir(input_fpath):
            generate_weight_cmds(input_fpath, odir)

        if os.path.isfile(input_fpath):
            if fname.endswith(warc_ext):
                output_fname = input_fpath.replace("/", "_")
                output_fname = output_fname[1:].lower()
                output_fpath = os.path.join(odir, output_fname)
                print("python extract_qapair_weight.py -ifname {} -ofname {}".format(input_fpath, output_fpath))
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-idir", type=str, help="The input directory", default=".")
    parser.add_argument("-odir", type=str, help="The output directory", default=".")
    args = parser.parse_args()

    input_dir = args.idir
    output_dir = args.odir
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generate_weight_cmds(input_dir, output_dir)

