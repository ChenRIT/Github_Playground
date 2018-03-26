# Input: an input directory and an output directory
# Output: All the plain-text versions of .warc.gz files in the input directory

import os
import sys
import argparse
import warc
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')


def warc_to_text(idir, odir):
    warc_ext = '.warc.gz'
    all_fnames = os.listdir(idir)
    
    for fname in all_fnames:
        input_fpath = os.path.join(idir, fname)
        output_fpath = os.path.join(odir, fname)
        if os.path.isdir(input_fpath):
            # Handle subdirectories
            if not os.path.exists(output_fpath):
                os.makedirs(output_fpath)
                warc_to_text(input_fpath, output_fpath)

        if os.path.isfile(input_fpath):
            # Handle files
            if fname.endswith(warc_ext):
                # Process warc files
                output_fname = output_fpath + ".txt"
                with open(output_fname, "w+") as ofile:
                    fwarc = warc.open(input_fpath, "rb")
                    for record in fwarc:
                        soup = BeautifulSoup(record.payload)
                        ofile.write(soup.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-idir", type=str, help="The input directory", default=".")
    parser.add_argument("-odir", type=str, help="The output directory", default=".")
    args = parser.parse_args()

    input_dir = args.idir
    output_dir = args.odir
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    warc_to_text(input_dir, output_dir)

