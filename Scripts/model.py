from ast import keyword
import pandas as pd
import spacy

from collections import Counter
from string import punctuation


MIN_KEYWORDS = 10

def get_keywords(model, text):
    result = []
    pos_tag = ['VERB', 'ADJ', 'NOUN']
    doc = model(text.lower())
    for token in doc:
        if(token.text in model.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
                
    return result


if __name__ == '__main__':
    sample_text = 'this is a sample sentence.'
    user_input = input('Enter a sentence to extract keywords from: ')

    model = spacy.load('en_core_web_md')

    input_text = user_input if user_input else sample_text
    keywords = get_keywords(model, input_text)

    print('\nTop 10 Keywords: \n')
    sorted_keywords = [x[0] for x in Counter(keywords).most_common(min(MIN_KEYWORDS, len(keywords)))]
    print(' '.join(sorted_keywords))
