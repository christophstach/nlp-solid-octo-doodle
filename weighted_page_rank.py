from typing import List, Callable

import numpy as np
import spacy

nlp = spacy.load('en')


class WeightedPageRank:
    def __init__(self, weights: List[List[float]], iterations: int):
        """
        Constructs the weighted pagerank.

        :param weights: The weights matrix between the nodes
        :param iterations: The number of iterations to use to loop over the dataset
        """
        self.weights = np.array(weights)
        self.iterations = iterations
        self.rankings = np.full(
            (1, self.weights.shape[0]),
            fill_value=1 / self.weights.shape[0]
        )

        for i in range(iterations - 1):
            self.iterate()

    def iterate(self) -> None:
        """
        Multiplies one time the weight matrix over the rankings of the previous
        iteration to calculate new scores.

        :return: None
        """
        # Add another row to the array
        self.rankings = np.vstack([
            self.rankings,
            np.dot(self.weights, self.rankings[-1])
        ])

    def sort_by_ranking(self, array: List[any]) -> List[any]:
        """
        Sorts an array based the on rankings of the last iteration.

        :param array: The array to sort
        :return: The sorted array
        """
        assert len(array) == len(self.rankings[-1])

        return [value for _, value in sorted(zip(self.rankings[-1], array), reverse=True)]


def build_weights_matrix(tokens: List[str],
                         comparator: Callable[[str, str], float],
                         normalize: bool = True) -> List[List[float]]:
    """
    Builds a weight matrix using the given comparator. Optionally normalizes each row of the matrix to the sum of one.

    :param tokens:
    :param comparator:
    :param normalize:
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

    :param text:
    :return:
    """
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def extract_words(text: str, remove_stopwords: bool = True) -> List[str]:
    """

    :param text:
    :param remove_stopwords:
    :return:
    """
    doc = nlp(text)

    words = [token.text for token in doc]
    words = list(filter(lambda word: not nlp.vocab[word].is_stop, words)) if remove_stopwords else words
    words = list(filter(lambda word: word not in ['.', '\n', ',', '?', '!', ';'], words))
    return words


def extract_noun_chunks(text: str) -> List[str]:
    """

    :param text:
    :return:
    """
    doc = nlp(text)

    return [chunk.text.lower() for chunk in doc.noun_chunks]


def spacy_similarity(token1: str, token2: str) -> float:
    """

    :param token1:
    :param token2:
    :return:
    """
    doc1 = nlp(token1)
    doc2 = nlp(token2)

    return doc1.similarity(doc2)


def softmax(x: List[float]) -> List[float]:
    """
    Compute softmax values for each sets of scores in x.

    :param x:
    :return:
    """
    exp = np.exp(x - np.max(x))

    return exp / exp.sum()
