import spacy

from models import NounChunkModel

print('')
print('')
print('')
print('Loading SpaCy...')
nlp = spacy.load('de')

print('Training for NounChunkModel...')
print('-----------------------------------------')
print('')
nc = NounChunkModel(nlp)
nc.fetch_database_articles()
nc.preprocess()
nc.create_dict()
nc.create_bow_corpus()
nc.train_w2v()
nc.train_d2v()
nc.train_tfidf()
