# Input: an input directory and an output directory
# Output: All the plain-text versions of .warc.gz files in the input directory

import os
import sys
import argparse
import warc
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

def warc_to_text(idir, odir, lfile, processed_files):
    warc_ext = '.warc.gz'
    all_fnames = os.listdir(idir)
    
    for fname in all_fnames:
        input_fpath = os.path.join(idir, fname)
        output_fpath = os.path.join(odir, fname)
        #print("Current file: {}".format(input_fpath))
        if os.path.isdir(input_fpath):
            # Handle subdirectories
            if not os.path.exists(output_fpath):
                os.makedirs(output_fpath)
                warc_to_text(input_fpath, output_fpath, lfile, processed_files)

        if os.path.isfile(input_fpath):
            # Handle files
            if fname.endswith(warc_ext):
                # Make sure the file has not been processed before
                if input_fpath in processed_files:
                    print("Jump processed files: {}".format(input_fpath))
                    continue
                
                # Process warc files
                output_fname = output_fpath + ".txt"
                with open(output_fname, "w+") as ofile:
                    fwarc = warc.open(input_fpath, "rb")
                    for record in fwarc:
                        soup = BeautifulSoup(record.payload)
                        ofile.write(soup.text)
                lfile.write(input_fpath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-idir", type=str, help="The input directory", default=".")
    parser.add_argument("-odir", type=str, help="The output directory", default=".")
    parser.add_argument("-l", "--log", type=str, help="The name of the log file", default="./log.txt")        
    args = parser.parse_args()

    input_dir = args.idir
    output_dir = args.odir
    log_fname = args.log
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    processed_files = []
    with open(log_fname, "r+") as lfile:
            for line in lfile:
                print("The file to skip: {}".format(line))
                processed_files.append(line[:-1])
            warc_to_text(input_dir, output_dir, lfile, processed_files)

