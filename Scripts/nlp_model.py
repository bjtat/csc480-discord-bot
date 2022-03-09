from ast import keyword
import pandas as pd
import spacy

from collections import Counter
from string import punctuation


MIN_KEYWORDS = 10

def get_keywords(model, text):
    result = []
    # pos_tag = ['VERB', 'ADJ', 'NOUN']
    doc = model(text.lower())
    for token in doc:
        if(token.text in model.Defaults.stop_words or token.text in punctuation):
            continue
        result.append(token.text)
                
    return result


if __name__ == '__main__':
    sample_text = 'Robin, create a new branch please'

    model = spacy.load('./model_output/model-last')

    keywords = get_keywords(model, sample_text)
    print(keywords)
