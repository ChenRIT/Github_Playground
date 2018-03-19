# Convert a ClueWeb warc file into a text file

import sys
import warc
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    input_file = "./00.warc.gz"
    output_fname = "./web_contents.txt"
    with open(output_fname, "w+") as ofile:
        fwarc = warc.open(input_file, "rb")
        for record in fwarc:
            soup = BeautifulSoup(record.payload)
            ofile.write(soup.text)
