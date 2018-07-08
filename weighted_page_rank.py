from typing import List

import numpy as np


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
