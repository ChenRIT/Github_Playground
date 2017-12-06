# Process ClueWeb with regular expression

import warc
import re

def extract_names_warc(warc_fname, output_file):
    fwarc = warc.open(warc_fname, "rb")

    #count = 0
    for record in fwarc:
        # if count > 1000:
        #     break
        # else:
        #     count += 1
        
        if record['Warc-type'] == 'warcinfo':
            pass
        else:
            name_pattern = [r'(I\'m\s([A-Z]\w+))',
                            r'(I\sam\s([A-Z]\w+))',
                            r'(This\sis\s([A-Z]\w+))',
                            r'(This\'s\s([A-Z]\w+))',
                            r'(My\sname\sis\s([A-Z]\w+))',
                            r'(The\sname\sis\s([A-Z]\w+))',
                            r'(\w+call\sme\s([A-Z]\w+))',
                            r'(I\'m\scalled\s([A-Z]\w+))']
            for reg in name_pattern:
                results = re.findall(reg, record.payload)
                if results:
                    for res in results:
                        output_file.write(str(res)+"\n")

if __name__ == "__main__":
    input_file = "./00.warc.gz"
    output_fname = "./name_patterns.txt"
    with open(output_fname, "a+") as ofile:
        extract_names_warc(input_file, ofile)
