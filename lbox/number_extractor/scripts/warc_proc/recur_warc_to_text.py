# Input: a directory name
# Output: a file containing all lines of name introduction

import os
import sys
import argparse
import warc
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')


def warc_to_text(dir):
    """ Extract phrases that introduce names from all warc files under dir"""
    warc_ext = '.warc.gz'
    all_fnames = os.listdir(dir)
    
    for fname in all_fnames:
        file_path = os.path.join(dir, fname)
        if os.path.isdir(file_path):
            # Handle subdirectories
            warc_to_text(file_path)

        if os.path.isfile(file_path):
            # Handle files
            if fname.endswith(warc_ext):
                # Process warc files
                output_fname = fname + ".txt"
                with open(output_fname, "w+") as ofile:
                    fwarc = warc.open(file_path, "rb")
                    for record in fwarc:
                        soup = BeautifulSoup(record.payload)
                        ofile.write(soup.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Parse all .warc.gz files in the directory
    dir = "/mnt/data/dataset/clueweb09/disk01/ClueWeb09_English_1/en0000"
    warc_to_text(dir)

