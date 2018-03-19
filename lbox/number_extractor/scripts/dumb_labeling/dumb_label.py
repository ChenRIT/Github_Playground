import sys
import csv
import re

import spacy
from spacy.symbols import NUM

nlp = spacy.load('en')

def separate_numbers(sent):
  # Separate numbers and its following words, e.g., 6.99you
  for m in re.findall("(\D*)(\d?[0-9\,\.]*\d)(\D*)", sent):
    m = [x for x in m if x]
    sent = sent.replace(''.join(m), ' ' + ' '.join(m) + ' ')
    sent = ' '.join(sent.split())
  return sent

if __name__ == "__main__":
    # Read input sentences
    input_fname = "./test.complicated.csv"
    # input_fname = "./test.annotated.csv"      
    raw_sents = []
    with open(input_fname) as pfile:
        sents_csv = csv.reader(pfile)
        for row in sents_csv:
            if row:
              raw_sents.append(row[0:2])
    raw_sents = raw_sents[1:] # The first row is the schema
    
    labeled_sents = []
    for ele in raw_sents:
      idx = ele[0]
      line = ele[1]
      new_line = separate_numbers(line)
      # Get the first number as both lower bound and upper bound
      # Get the token after "per" as the rate
      nlp_line = nlp(new_line)
      num_label = "-"
      rate = "-"
      is_rate = False
      num_extracted = False
      for token in nlp_line:
        if is_rate:
          rate = token.text
          is_rate = False
          
        if not num_extracted and token.pos == NUM:
          num_label = token
          num_extracted = True
              
        if token.text == "per":
          is_rate = True
              
      # Always output "$" as currency
      currency_label = "$"

      labeled_sents.append([idx, line, num_label, num_label, currency_label, rate])

    output_fname = "./label_data.csv"
    with open(output_fname, 'w') as ofile:
      sentwriter = csv.writer(ofile)
      sentwriter.writerow(['index', 'sentence', 'LB', 'UB', 'Currency', 'Rate'])
      for ele in labeled_sents:
        sentwriter.writerow(ele)
            
