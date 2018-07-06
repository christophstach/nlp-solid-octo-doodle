from typing import List

import numpy as np
import spacy
from pprint import pprint


nlp = spacy.load('de')


def softmax(x):
    """
        Compute softmax values for each sets of scores in x.
    """
    exp = np.exp(x - np.max(x))

    return exp / exp.sum()


class Node:
    def __init__(self, identifier: int or float or str):
        self.identifier = identifier


class Edge:
    def __init__(
            self,
            from_node_identifier: int or float or str,
            to_node_identifier: int or float or str,
            weight: float = 1.0
    ):
        self.from_node_identifier = from_node_identifier
        self.to_node_identifier = to_node_identifier
        self.weight = weight

    def __repr__(self):
        return '{0} -({1})-> {2}'.format(self.from_node_identifier, self.weight, self.to_node_identifier)


class Graph:
    def __init__(self, nodes: List[Node], edges: List[Edge]):
        self.nodes = nodes
        self.edges = edges

    def get_edges_to(self, node_identifier: int or float or str):
        return list(filter(lambda edge: edge.to_node_identifier == node_identifier, self.edges))

    def get_edges_from(self, node_identifier: int or float or str):
        return list(filter(lambda edge: edge.from_node_identifier == node_identifier, self.edges))

    def get_weight(self, node1_identifier: int or float or str, node2_identifier: int or float or str):
        return list(filter(
            lambda edge: edge.from_node_identifier == node1_identifier and edge.to_node_identifier == node2_identifier,
            self.edges
        ))[0].weight


class Page:
    def __init__(
            self,
            identifier: int or float or str,
            links_to: List[int or float or str],
            weights: List[float] = None
    ):
        self.identifier = identifier
        self.links_to = links_to
        self.weights = weights

    def __repr__(self):
        return 'Page({0})[{1}]'.format(self.identifier, ', '.join(self.links_to))


class Rank:
    def __init__(self, node_identifier, rank: float):
        self.node_identifier = node_identifier
        self.rank = rank

    def __repr__(self):
        return '{0}: {1}'.format(self.node_identifier, self.rank)


class PageRank:
    def __init__(self, pages: List[Page], weights: List[List[float]] = None):
        self.pages = pages
        self.iteration: int = 0
        self.ranks: List[List[Rank]] = []
        self.graph: Graph = None
        self.weights: List[List[float]] = [softmax(weight) for weight in weights]

    def build_graph(self):
        nodes: List[Node] = []
        edges: List[Edge] = []

        for pageIndex, page in enumerate(pages):
            nodes.append(Node(page.identifier))

            if self.weights:
                for (link, weight) in zip(page.links_to, self.weights[pageIndex]):
                    edges.append(Edge(page.identifier, link, weight))
            else:
                for link in page.links_to:
                    edges.append(Edge(page.identifier, link))

        self.graph = Graph(nodes, edges)

    def iterate(self):
        if self.iteration == 0:
            current_iteration: List[Rank] = []
            for node1 in self.graph.nodes:
                current_iteration.append(
                    Rank(node1.identifier, 1 / len(self.graph.nodes))
                )

            self.ranks.append(current_iteration)
        else:
            current_iteration: List[Rank] = []
            for node in self.graph.nodes:
                new_rank = 0
                for edge in self.graph.get_edges_to(node.identifier):
                    new_rank += (
                                        self.get_last_rank(edge.from_node_identifier)
                                        /
                                        len(self.graph.get_edges_from(edge.from_node_identifier))
                                ) * edge.weight

                current_iteration.append(
                    Rank(node.identifier, new_rank)
                )
            self.ranks.append(current_iteration)

        self.iteration += 1

    def get_last_rank(self, node_identifier: int or float or str):
        return list(filter(
            lambda rank: rank.node_identifier == node_identifier,
            self.ranks[self.iteration - 1]
        ))[0].rank

    def get_pagerank(self):
        for i in range(len(self.graph.nodes)):
            self.iterate()

    def get_weight_matrix(self, text):

        doc = nlp(text)

        sents = [sent.text for sent in doc.sents]
        matrix = []

        for y, sentY in enumerate(sents):
            matrix.append([])
            for x, sentX in enumerate(sents):
                matrix[y].append(self.similarity(sentY, sentX))


        pprint(matrix)

    def similarity(self, text1, text2):
        docX = nlp(text1)
        docY = nlp(text2)

        return docX.similarity(docY)


pages: List[Page] = [
    Page('A', ['B', 'C']),
    Page('B', ['D']),
    Page('C', ['A', 'B', 'D']),
    Page('D', ['C'])
]

pages: List[Page] = [
    Page('A', ['B', 'C']),
    Page('B', ['A', 'C']),
    Page('C', ['A', 'B'])
]

pageRank: PageRank = PageRank(pages, [
    [0.2, 0.7],
    [0.2, 0.4],
    [0.7, 0.4]
])

pageRank.get_weight_matrix(text)

# pageRank.build_graph()
# pageRank.iterate()
# pageRank.iterate()
# pageRank.iterate()
# pageRank.iterate()
# pageRank.iterate()
# pageRank.iterate()

# print(pageRank.ranks[0])
# print(pageRank.ranks[1])
# print(pageRank.ranks[2])
# print(pageRank.ranks[3])
# print(pageRank.ranks[4])
# print(pageRank.ranks[1])
# print(pageRank.ranks[2])
# print(pageRank.ranks[3])
