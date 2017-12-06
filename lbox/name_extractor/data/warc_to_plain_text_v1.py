# Convert a ClueWeb warc file into a text file

import sys
import warc
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

def write_tag_to_file(ofile, soup, tag):
    ''' Write the contents of the tag to an output file '''
    if soup is not None:
        tag_contents = soup.find_all(tag)
        for cont in tag_contents:
            if cont.string is not None:
                ofile.write(cont.string)

def print_contents(soup, tag):
    ''' Print the top fifty contents of tag '''
    if soup is not None:
        tag_contents = soup.find_all(tag)
        for cont in tag_contents:
            if cont.string is not None:
                print cont.string

if __name__ == "__main__":
    input_file = "./00.warc.gz"
    output_fname = "./web_contents.txt"
    with open(output_fname, "w+") as ofile:
        fwarc = warc.open(input_file, "rb")
        for record in fwarc:
            soup = BeautifulSoup(record.payload)
            write_tag_to_file(ofile, soup, 'p')
            #print_contents(soup, 'p')
            #print_contents(soup, 'pre')            
