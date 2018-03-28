# Convert a ClueWeb warc file into a text file

import sys
import warc
import argparse
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ifname", type=str, help="The input file", default="")
    parser.add_argument("-ofname", type=str, help="The output file", default="")
    args = parser.parse_args()
    
    input_file = args.ifname
    output_fname = args.ofname
    with open(output_fname, "w+") as ofile:
        fwarc = warc.open(input_file, "rb")
        for record in fwarc:
            soup = BeautifulSoup(record.payload)
            ofile.write(soup.text)
