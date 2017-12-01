# Process ClueWeb with regular expression

import warc
import re

def extract_names_warc(warc_file, output_file):
    fwarc = warc.open(warc_file, "rb")

    with open(output_file, "a+") as ofile:
        count = 0
        for record in fwarc:
            if count > 1000:
                break
            else:
                count += 1
            
            if record['Warc-type'] == 'warcinfo':
                pass
            else:
                name_pattern = r'I\'m\s[A-Z]\w+|I\sam\s\[A-Z]w+|This\sis\s[A-Z]\w+|This\'s\s[A-Z]\w+|My\sname\sis\s[A-Z]\w+|The\sname\sis\s[A-Z]\w+|\w+call\sme\s[A-Z]\w+|I\'m\scalled\s[A-Z]\w+'
                results = re.findall(name_pattern, record.payload)
                if results:
                    for res in results:
                        ofile.write(res+"\n")

if __name__ == "__main__":
    input_file = "./00.warc.gz"
    output_file = "./name_patterns.txt"
    extract_names_warc(input_file, output_file)
