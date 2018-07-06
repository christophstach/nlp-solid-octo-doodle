from datetime import datetime
from time import sleep

from gensim.corpora import Dictionary, MmCorpus
from gensim.models import Word2Vec, Doc2Vec, TfidfModel
from gensim.models.doc2vec import TaggedDocument

from database import GetArticles
from preprocessors import NounChunkPreprocessor
import pickle


class NounChunkModel:
    def __init__(self, nlp: any):
        self.nlp = nlp
        self.articles = None
        self.preprocessed_articles = None
        self.preprocessed_article_texts = None
        self.bow_corpus = None
        self.verbose: bool = True
        self.preprocessing_strategy = 'noun-chunks'

        self.w2v_file = './data/' + self.preprocessing_strategy + '/w2v.bin'
        self.d2v_file = './data/' + self.preprocessing_strategy + '/d2v.bin'
        self.dict_file = './data/' + self.preprocessing_strategy + '/dict.bin'
        self.tfidf_file = './data/' + self.preprocessing_strategy + '/tfidf.bin'
        self.bow_corpus_file = './data/' + self.preprocessing_strategy + '/bow-corpus.mm'
        self.preprocessed_articles_file = './data/' + self.preprocessing_strategy + '/preprocessed-articles.pkl'
        self.preprocessed_article_texts_file = './data/' + self.preprocessing_strategy \
                                               + '/preprocessed-article-texts.pkl'

        self.w2v: Word2Vec = None
        self.d2v: Doc2Vec = None
        self.dict: Dictionary = None
        self.tfidf: TfidfModel = None
        pass

    def log(self, text):
        if self.verbose:
            print('[' + datetime.now().__format__('%H:%M:%S') + ']:', text)

    def fetch_database_articles(self, local=False, test_run=False):
        self.log('Fetching articles from database...')
        self.articles = GetArticles(local=local, test_run=test_run)

        sleep(2)

    def preprocess(self, persist=True):
        self.log('Preprocessing texts...')

        sleep(2)
        preprocessor = NounChunkPreprocessor(nlp=self.nlp, use_tqdm=self.verbose)
        self.preprocessed_articles = preprocessor.preprocess(self.articles)
        self.preprocessed_article_texts = list(map(lambda article: article['text'], self.preprocessed_articles))
        sleep(2)

        if persist:
            self.log('Saving preprocessed articles to disk for future use...')
            with open(self.preprocessed_articles_file, 'wb') as f:
                pickle.dump(self.preprocessed_articles, f)
                sleep(2)

            self.log('Saving preprocessed article texts to disk for future use...')
            with open(self.preprocessed_article_texts_file, 'wb') as f:
                pickle.dump(self.preprocessed_article_texts, f)
                sleep(2)

    def create_dict(self, persist=True):
        self.log('Creating dictionary...')
        self.dict = Dictionary(self.preprocessed_article_texts)

        if persist:
            self.log('Saving dictionary to disk for future use...')
            self.dict.save(self.dict_file)
            sleep(2)

    def create_bow_corpus(self, persist=True):
        self.log('Making Bag-of-Words corpus...')
        self.bow_corpus = list(map(self.dict.doc2bow, self.preprocessed_article_texts))
        sleep(2)

        if persist:
            self.log('Saving Bag-of-Words corpus to disk for future use...')
            MmCorpus.serialize(self.bow_corpus_file, self.bow_corpus)
            sleep(2)

    def train_w2v(self, persist=True):
        self.log('Training word2vec model...')
        self.w2v = Word2Vec(sentences=self.preprocessed_article_texts, window=4, min_count=2, size=300)

        sleep(2)

        if persist:
            self.log('Saving word2vec model to disk for future use...')
            self.w2v.save(self.w2v_file)

            sleep(2)

    def train_d2v(self, persist=True):
        self.log('Training doc2vec model...')
        tagged_documents = list(map(
            lambda article: TaggedDocument(words=article['text'], tags=[str(article['_id'])]),
            self.preprocessed_articles
        ))
        self.d2v = Doc2Vec(documents=tagged_documents, window=4)

        sleep(2)

        if persist:
            self.log('Saving doc2vec model to disk for future use...')
            self.d2v.save(self.d2v_file)

            sleep(2)

    def train_tfidf(self, persist=True):
        self.tfidf = TfidfModel(self.bow_corpus)  # fit model

        sleep(2)

        if persist:
            self.log('Saving TfIdf model to disk for future use...')
            self.tfidf.save(self.tfidf_file)

            sleep(2)
