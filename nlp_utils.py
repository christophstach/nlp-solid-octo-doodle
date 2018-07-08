from typing import List, Callable

import numpy as np
import spacy

nlp = spacy.load('de')


def build_weights_matrix(tokens: List[str],
                         comparator: Callable[[str, str], float],
                         normalize: bool = True) -> List[List[float]]:
    """
    Builds a weight matrix using the given comparator. Optionally normalizes each row of the matrix to the sum of one.

    :param tokens: The tokens to compare
    :param comparator: A function to compare the tokens
    :param normalize: Should the matrix be column normalized
    :return:
    """
    weights = []

    for i, token1 in enumerate(tokens):
        weights.append([])
        for o, token2 in enumerate(tokens):
            if i == o:
                weights[i].append(0)
            else:
                weights[i].append(comparator(token1, token2))

    weights = np.array(weights)

    if normalize:
        weights = [softmax(weightRow) for weightRow in weights.T]
        weights = np.array(weights).T

    return weights


def extract_sentences(text: str) -> List[str]:
    """
    Extracts all sentences from the text

    :param text: A text to split in sentences
    :return: A list of sentences
    """
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def extract_words(text: str, remove_stopwords: bool = True) -> List[str]:
    """
    Extracts all words from the text

    :param text: The text to split into words
    :param remove_stopwords: Should top words be removed
    :return: A list of words
    """
    doc = nlp(text)

    words = [token.text for token in doc]
    words = list(filter(lambda word: not nlp.vocab[word].is_stop, words)) if remove_stopwords else words
    words = list(filter(lambda word: word not in ['.', '\n', ',', '?', '!', ';'], words))
    return words


def extract_noun_chunks(text: str) -> List[str]:
    """
    Extract all noun chunks from a text

    :param text: The text to split into noun chunks
    :return: A list of noun chunks
    """
    doc = nlp(text)

    return [chunk.text for chunk in doc.noun_chunks]


def spacy_similarity(token1: str, token2: str) -> float:
    """
    Calculates the similarity between two tokens using the native spacy similarity function

    :param token1: Token 1 to compare
    :param token2: Token 2 to compare
    :return: The similarity between the tokens
    """
    doc1 = nlp(token1)
    doc2 = nlp(token2)

    return doc1.similarity(doc2)


def softmax(x: List[float]) -> List[float]:
    """
    Compute softmax values for each sets of scores in x.

    :param x: A vector of values
    :return: The softmax normalized vector
    """
    exp = np.exp(x - np.max(x))

    return exp / exp.sum()
