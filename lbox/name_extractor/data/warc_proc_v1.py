# Process ClueWeb with spaCy

import warc
import spacy

nlp = spacy.load('en')
f = warc.open("00.warc.gz", "rb")

for record in f:
    if record['Warc-type'] == 'warcinfo':
        pass
    else:
        if "My name" in record.payload:
            doc = nlp(record.payload.decode('utf-8', 'ignore'))
            for sent in doc.sents:
                if "My name" in sent.text:
                    print sent.text
                    
