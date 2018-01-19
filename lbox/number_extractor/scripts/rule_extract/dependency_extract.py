import argparse

import spacy
from spacy.lang.en import English
from spacy.symbols import NUM

nlp = spacy.load('en')

test_strings = ["At Sacramento's Caesar Chavez Park farmers market, cherries are between $4 and $6 a pound.",
                "The cryptocurrency hit a record high when it passed the $19850 mark in mid-December, but tumbled rapidly, falling to below $12000 within days.",
                "The medium home price in this area is 1 million.",
                "It will take longer to sell, and an educated buyer is going to want at least $10g taken off the price, \
                 when the repairs have been completed…and more if they haven’t.",
                "bsite have been nicely compiled according to there price ranges such as those that amount less than $70, or between $70- $100, or those amounting to more than $1000 have been put under one category.",
                "It costs me around 3 hundred bucks.",
                "The price range is from 3 million to 6 million yen."]

# test_strings = ["It costs me around 3 hundred bucks."]

units = ['dollar', 'buck', 'yen', 'yuan']

def extract_numerical_value(raw_sentence):
    doc = nlp(raw_sentence)
    extraction_result = []
    is_head = True
    for token in doc:
        for unit in units:
            if unit in token.text:
                # token_list = extract_offspring(token)
                token_list = [child for child in token.subtree]
                extraction_result.append(token_list)
                break

    for token in doc:
        if token.pos == NUM:
            is_head = True
            is_extract = False

            # Make sure the number is not children of any other number
            for tk in token.ancestors:
                if tk.pos == NUM:
                    is_head = False
                    break
                else:
                    continue

            if is_head == True:
                # Make sure the token hasn't been extracted before
                # print("Token: {}".format(token.text))
                # print("Extracted tokens: {}".format(extraction_result))
                for extraction in extraction_result:
                    for extk in extraction:
                        if token == extk:
                            is_extract = True
                            break
                    if is_extract:
                        break
                if is_extract:
                    continue

                # token_list = extract_offspring(token)
                token_list = [child for child in token.subtree]
                extraction_result.append(token_list)
            else:
                continue
        else:
            continue

    return extraction_result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sentence", type=str, help="The user utterance", default=None)
    parser.add_argument("-t", "--test", type=int, help="1: use test strings. 0: do not use.", default=0)    
    args = parser.parse_args()

    results = {}

    input_string = args.sentence
    if input_string:
        test_res = extract_numerical_value(input_string)
        res = extract_numerical_value(input_string)
        results[input_string] = res

    in_test_mode = args.test
    if in_test_mode:
        for sent in test_strings:
            res = extract_numerical_value(sent)
            results[sent] = res
        
    for key, value in results.items():
        print(key)
        print(value)
        print('\n')

    # print("Dependency parsing results: \n")
    # for token in nlp(test_string):
    #     print(token.text, token.pos_, token.dep_, [child for child in token.children])
