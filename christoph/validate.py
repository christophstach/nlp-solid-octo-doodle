from statistics import mean, median
from time import sleep

import spacy
from gensim.corpora import Dictionary
from gensim.matutils import softcossim
from gensim.models import Word2Vec, TfidfModel
from tqdm import tqdm

from preprocessors import NounChunkPreprocessor
from validation_data import get_train, get_test

print('Loading spaCy...')
nlp = spacy.load('de')

print('Loading models...')
word2vec = Word2Vec.load('./data/noun-chunks.w2v.bin')
dictionary = Dictionary.load('./data/noun-chunks.dict.bin')
tfidf = TfidfModel.load('./data/noun-chunks.tfidf.bin')

print('Creating similarity matrix...')
similarity_matrix = word2vec.wv.similarity_matrix(dictionary, tfidf)
preprocessor = NounChunkPreprocessor(nlp=nlp)


def is_duplicate(text1, text2, threshold):
    preprocessed_text1 = preprocessor.preprocess_text(data['text1'])
    preprocessed_text2 = preprocessor.preprocess_text(data['text2'])

    bow1 = dictionary.doc2bow(preprocessed_text1)
    bow2 = dictionary.doc2bow(preprocessed_text2)

    softcossim_similarity = softcossim(bow1, bow2, similarity_matrix)

    return softcossim_similarity >= threshold


print('')
print('#################################################################')
print('')

duplicates = []
none_duplicates = []

train = get_train()

for data in tqdm(train, desc='Calculating similarities'):
    preprocessed_text1 = preprocessor.preprocess_text(data['text1'])
    preprocessed_text2 = preprocessor.preprocess_text(data['text2'])

    bow1 = dictionary.doc2bow(preprocessed_text1)
    bow2 = dictionary.doc2bow(preprocessed_text2)

    softcossim_similarity = softcossim(bow1, bow2, similarity_matrix)

    if data['duplicate']:
        duplicates.append(softcossim_similarity)
    else:
        none_duplicates.append(softcossim_similarity)

sleep(2)
print('Mean duplicates:', mean(duplicates))

print()

mean_duplicates = mean(duplicates)

test = get_test()
correct = 0
total = len(test)

for data in tqdm(test, desc='Calculating duplicates'):
    if data['duplicate'] == is_duplicate(data['text1'], data['text2'], mean_duplicates):
        correct += 1

sleep(2)
print('Correct: ', correct)
print('Total: ', total)
print('Accuracy: ', (correct / total * 100), '%')
