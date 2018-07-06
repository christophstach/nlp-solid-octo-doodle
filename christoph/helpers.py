import re

import spacy
from spacy.symbols import NOUN

nlp = spacy.load('de')


def to_lower(list_of_words):
    return [word.lower() for word in list_of_words]


def clean(text):
    text = re.sub(' +', ' ', text)
    text = re.sub(r'[^\w äöüÄÖÜß\"\:\,\.?\!\-\_ ]', '', text)
    text = re.sub(' 0 0 ', '', text)
    text = re.sub('Mehr zum Thema\:(.*)', '', text)
    text = re.sub('Berliner Morgenpost [0-9]{4} (.*) Alle Rechte vorbehalten\.', '',
                  text)  # removes copyright if 'Mehr zum Thema' is not in text
    text = re.sub('&', 'und', text)
    text = re.sub(' +', ' ', text)
    text = re.sub(' \.', '.', text)
    text = re.sub('Berliner Morgenpost [0-9]{4} Alle Rechte vorbehalten\.', '', text)
    text = text.strip()

    return text


def remove_punctation(text):
    return re.sub('[.?!":,\']', '', text)


def to_sentences(text):
    doc = nlp(text)
    return [sentence.text for sentence in doc.sents]


def to_words(text):
    doc = nlp(text)
    return [token.text for token in doc]


def min_word_count(text):
    return len(to_words(text)) > 4


def min_token_count(text):
    return text is not None and len(text) > 4


def flatten(array):
    new_array = []

    for value in array:
        for inner_value in value:
            new_array.append(inner_value)

    return new_array


def to_hierarchical_phrases(text):
    doc = nlp(text)
    tokens = []

    for token in doc:
        if token.pos == NOUN:
            tokens.append(token.text)
            tokens.append(token.head.text)

    return tokens


def to_noun_phrases(text):
    doc = nlp(text)
    return [chunk.text for chunk in doc.noun_chunks]


def split_noun_phrases(list_of_chunks):
    words = []

    for chunk in list_of_chunks:
        doc = nlp(chunk)
        words.append([word.text for word in doc])

    return flatten(words)


def remove_stop_words(list_of_words):
    sentence = ' '.join(list_of_words)
    doc = nlp(sentence)
    tokens = [token for token in doc]
    tokens = list(filter(lambda token: token.is_stop == False, tokens))
    words = list(map(lambda token: token.text, tokens))

    return words


def to_lower(list_of_words):
    return [word.lower() for word in list_of_words]


def is_stop_word(word):
    return nlp.Defaults.stop_words[word]
