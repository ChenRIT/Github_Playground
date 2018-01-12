import spacy

nlp = spacy.load('en')
tokenizer = spacy.tokenizer.Tokenizer(nlp.vocab)

def extract_num_chunk(sent):
    '''
    Extract the number chunks from a sentence

    @return: a list of number chunks. Each number chunk is represented by a pair (starting index, ending index)

    '''

    # Tokenize the sentence
    doc = nlp(sent)
    tokens = tokenizer(sent)

    # Find sequences of numbers
    num_chunks = []
    token_start = None
    for token in tokens:
        if token.like_num:
            if token_start is None:
                token_start = token.i
            else:
                continue
        else:
            if token_start is None:
                continue
            else:
                num_chunks.append((token_start, token.i))
                #print(token.text)
                #print("Add: {}".format(num_chunks))
                token_start = None

    if token_start:
        num_chunks.append((token_start, len(doc)))

    return num_chunks

def decode_num_chunk(chunk_pair, sent):
    '''
    Textual representation of the number chunk

    '''

    # Tokenize the sentence
    doc = nlp(sent)
    tokens = tokenizer(sent)

    # Generate textual representation
    num_tokens = []
    num_start, num_end = chunk_pair

    return doc[num_start:num_end].text

if __name__ == "__main__":
    test_string = "I have a 2005 five car which costs me 3 hundred thousand dollars."

    num_chunk_idx = extract_num_chunk(test_string)
    for num_tokens in num_chunk_idx:
        #print(num_tokens)
        print(decode_num_chunk(num_tokens, test_string))
