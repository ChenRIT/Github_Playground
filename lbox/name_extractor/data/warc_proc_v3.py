# Process ClueWeb with regular expression

import warc
import re

def extract_names_warc(warc_fname, output_file):
    fwarc = warc.open(warc_fname, "rb")

    for record in fwarc:
        if record['Warc-type'] == 'warcinfo':
            pass
        else:
            name_pattern = r'I\'m\s[A-Z]\w+|I\sam\s\[A-Z]w+|This\sis\s[A-Z]\w+|This\'s\s[A-Z]\w+|My\sname\sis\s[A-Z]\w+|The\sname\sis\s[A-Z]\w+|\w+call\sme\s[A-Z]\w+|I\'m\scalled\s[A-Z]\w+'
            results = re.findall(name_pattern, record.payload)
            if results:
                for res in results:
                    output_file.write(res+"\n")

if __name__ == "__main__":
    input_file = "./00.warc.gz"
    output_fname = "./name_patterns.txt"
    with open(output_fname, "a+") as ofile:
        extract_names_warc(input_file, ofile)
