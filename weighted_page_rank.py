from typing import List, Callable

import numpy as np
import spacy

nlp = spacy.load('en')


class WeightedPageRank:
    def __init__(self, weights, iterations):
        self.weights = np.array(weights)
        self.iterations = iterations
        self.rankings = np.full(
            (1, self.weights.shape[0]),
            fill_value=1 / self.weights.shape[0]
        )

        for i in range(iterations - 1):
            self.iterate()

    def iterate(self):
        # Add another row to the array
        self.rankings = np.vstack([
            self.rankings,
            np.dot(self.weights, self.rankings[-1])
        ])

    def sort_by_ranking(self, arr: List[any]) -> List[any]:
        assert len(arr) == len(self.rankings[-1])

        return [value for _, value in sorted(zip(self.rankings[-1], arr), reverse=True)]


def build_weights_matrix(tokens: List[str], comparator: Callable[[str, str], float], normalize: bool = True):
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
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def extract_words(text: str, remove_stopwords: bool = True) -> List[str]:
    doc = nlp(text)

    words = [token.text.lower() for token in doc]

    words = list(filter(lambda word: not nlp.vocab[word].is_stop, words)) if remove_stopwords else words
    words = list(filter(lambda word: word not in ['.', '\n', ','], words))
    return words


def spacy_similarity(token1: str, token2: str) -> float:
    doc1 = nlp(token1)
    doc2 = nlp(token2)

    return doc1.similarity(doc2)


def softmax(x):
    """
        Compute softmax values for each sets of scores in x.
    """
    exp = np.exp(x - np.max(x))

    return exp / exp.sum()
