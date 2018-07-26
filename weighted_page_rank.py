from typing import List
import time
import numpy as np


class WeightedPageRank:
    def __init__(self, weights: List[List[float]]):
        """
        Constructs the weighted pagerank.

        :param weights: The weights matrix between the nodes
        :param iterations: The number of iterations to use to loop over the dataset
        """
        self.weights = np.array(weights)
        self.epsilon = 1.0e-20
        self.rankings = np.full(
            (1, self.weights.shape[0]),
            fill_value=1 / self.weights.shape[0]
        )
        self.rankingLearn = np.zeros_like(self.rankings)
        difference = 1
        while difference > self.epsilon:
            self.iterate()
            difference = np.max(
                np.abs(np.subtract(self.rankings[-1], self.rankingLearn[-1]))
            )
            self.rankingLearn = self.rankings

    def iterate(self) -> None:
        """
        Multiplies one time the weight matrix over the rankings of the previous
        iteration to calculate new scores.
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

    def get_top_entries(self, array: List[any], count: int = 4, keep_original_occurrence: bool = True):
        """
        Returns the top entries of a given array based on the rankins

        :param array: The array
        :param count: The number of entries to return
        :param keep_original_occurrence: Should the original order of the entries in the text be preserved
        :return: The top entries based on the ranking
        """
        sorted_array = self.sort_by_ranking(array)
        sorted_array = sorted_array[0:count]

        if keep_original_occurrence:
            sorted_array = [value for _, value in sorted(
                zip(array, sorted_array), reverse=True)]

        return sorted_array
