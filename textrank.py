from pprint import pprint

from nlp_utils import build_weights_matrix, extract_sentences, extract_words, extract_noun_chunks, spacy_similarity
from weighted_page_rank import WeightedPageRank

text = '''Automatic summarization is the process of reducing a text document with a
computer program in order to create a summary that retains the most important points
of the original document. As the problem of information overload has grown, and as
the quantity of data has increased, so has interest in automatic summarization.
Technologies that can make a coherent summary take into account variables such as
length, writing style and syntax. An example of the use of summarization technology
is search engines such as Google. Document summarization is another.'''

print('''
####################################
# Summary                          #
####################################
''')
sentences = extract_sentences(text)
weights = build_weights_matrix(tokens=sentences, comparator=spacy_similarity, normalize=True)
pr = WeightedPageRank(weights=weights, iterations=len(sentences))
pprint(pr.sort_by_ranking(sentences))

print('''
####################################
# Keywords (words)                 #
####################################
''')
words = extract_words(text)
weights = build_weights_matrix(tokens=words, comparator=spacy_similarity, normalize=True)
pr = WeightedPageRank(weights=weights, iterations=len(words))
pprint(pr.sort_by_ranking(words))

print('''
####################################
# Keywords (noun chunks)           #
####################################
''')
noun_chunks = extract_noun_chunks(text)
weights = build_weights_matrix(tokens=noun_chunks, comparator=spacy_similarity, normalize=True)
pr = WeightedPageRank(weights=weights, iterations=len(noun_chunks))
pprint(pr.sort_by_ranking(noun_chunks))
