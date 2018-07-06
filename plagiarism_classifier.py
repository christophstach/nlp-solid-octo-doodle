from pprint import pprint

import plac
import random
import pathlib
import cytoolz
import numpy
import csv

from keras import Model, Input
from keras.models import Sequential, model_from_json
from keras.layers import LSTM, Dense, Embedding, Bidirectional, concatenate, Concatenate
from keras.layers import TimeDistributed
from keras.optimizers import Adam
import thinc.extra.datasets
from spacy.compat import pickle
import spacy


class PlagiarismAnalyser(object):
    @classmethod
    def load(cls, path, nlp, max_length=100):
        with (path / 'config.json').open() as file_:
            model = model_from_json(file_.read())
        with (path / 'model').open('rb') as file_:
            lstm_weights = pickle.load(file_)
        embeddings = get_embeddings(nlp.vocab)
        model.set_weights([embeddings] + lstm_weights)
        return cls(model, max_length=max_length)

    def __init__(self, model, max_length=100):
        self._model = model
        self.max_length = max_length

    def __call__(self, doc):
        X = get_features([doc], self.max_length)
        y = self._model.predict(X)
        self.set_plagiarism(doc, y)

    def pipe(self, docs, batch_size=1000, n_threads=2):
        for minibatch in cytoolz.partition_all(batch_size, docs):
            minibatch = list(minibatch)
            sentences = []
            for doc in minibatch:
                sentences.extend(doc.sents)
            Xs = get_features(sentences, self.max_length)
            ys = self._model.predict(Xs)
            for sent, label in zip(sentences, ys):
                sent.doc.sentiment += label - 0.5
            for doc in minibatch:
                yield doc

    def set_plagiarism(self, doc, y):
        doc.user_data['plagiarism'] = float(y[0])
        # Sentiment has a native slot for a single float.
        # For arbitrary data storage, there's:
        # doc.user_data['my_data'] = y


def get_labelled_sentences(docs, doc_labels):
    labels = []
    sentences = []
    for doc, y in zip(docs, doc_labels):
        for sent in doc.sents:
            sentences.append(sent)
            labels.append(y)
    return sentences, numpy.asarray(labels, dtype='int32')


def get_features(docs, max_length):
    docs = list(docs)
    Xs = numpy.zeros((len(docs), max_length, 128), dtype='float32')
    for i, doc in enumerate(docs):
        j = 0
        for token in doc:
            Xs[i, j] = token.vector
            j += 1
            if j >= max_length:
                break
    return Xs


def train(train_texts, train_texts2, train_labels, dev_texts, dev_labels,
          lstm_shape, lstm_settings, lstm_optimizer, batch_size=100,
          nb_epoch=5, by_sentence=True):
    print(len(train_texts))
    print(len(train_texts2))
    print("Loading spaCy")
    nlp = spacy.load('de_core_news_sm')
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    print(nlp.vocab)
    embeddings = nlp('Baum').vector                                         #Todo: Baum?
    model = compile_lstm(embeddings, lstm_shape, lstm_settings)
    print("Parsing texts...")
    train_docs = list(nlp.pipe(train_texts))
    train_docs2 = list(nlp.pipe(train_texts2))
    #pprint(train_docs2)
    #dev_docs = list(nlp.pipe(dev_texts))
    if by_sentence:
        train_docs, train_labels = get_labelled_sentences(train_docs, train_labels)
        #dev_docs, dev_labels = get_labelled_sentences(dev_docs, dev_labels)
    print(len(train_docs))
    print(len(train_docs2))
    train_X1 = get_features((train_docs), lstm_shape['max_length'])
    train_X2 = get_features((train_docs2), lstm_shape['max_length'])
    #dev_X = get_features(dev_docs, lstm_shape['max_length'])
    train_X2 = train_X1
    model.fit([train_X1,train_X2], train_labels,
              nb_epoch=nb_epoch, batch_size=batch_size)
    return model


def compile_lstm(embeddings, shape, settings):
    ids1 = Input(shape=(shape['max_length'],128), dtype='float32', name='doc1')
    print(ids1.shape)
    ids2 = Input(shape=(shape['max_length'],128), dtype='float32', name='doc2')
    concat = concatenate([ids1, ids2])
    time_distributed = TimeDistributed(Dense(shape['nr_hidden'], use_bias=False))(concat)
    biLSTM = Bidirectional(
        LSTM(shape['nr_hidden'], recurrent_dropout=settings['dropout'], dropout=settings['dropout']))(time_distributed)

    scores = Dense(1, activation='softmax')(biLSTM)

    model = Model(input=[ids1, ids2], outputs=scores)
    model.compile(optimizer=Adam(lr=settings['lr']), loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model


def get_embeddings(vocab):
    return vocab.vectors.data


def evaluate(model_dir, texts, labels, max_length=100):
    def create_pipeline(nlp):
        '''
        This could be a lambda, but named functions are easier to read in Python.
        '''
        return [nlp.tagger, nlp.parser, PlagiarismAnalyser.load(model_dir, nlp,
                                                                max_length=max_length)]

    nlp = spacy.load('de_core_news_sm')      #todo: determine model. was: 'en'
    nlp.pipeline = create_pipeline(nlp)

    correct = 0
    i = 0
    for doc in nlp.pipe(texts, batch_size=1000, n_threads=4):
        correct += bool(doc.sentiment >= 0.5) == bool(labels[i])
        i += 1
    return float(correct) / i


def read_data(data_dir, limit=0):
    examples = []
    with open(data_dir) as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            examples.append((row[0], row[1], row[2]))
    random.shuffle(examples)
    if limit >= 1:
        examples = examples[:limit]
    return zip(*examples)


@plac.annotations(
    train_dir=("Location of training file or directory"),
    dev_dir=("Location of development file or directory"),
    model_dir=("Location of output model directory",),
    is_runtime=("Demonstrate run-time usage", "flag", "r", bool),
    nr_hidden=("Number of hidden units", "option", "H", int),
    max_length=("Maximum sentence length", "option", "L", int),
    dropout=("Dropout", "option", "d", float),
    learn_rate=("Learn rate", "option", "e", float),
    nb_epoch=("Number of training epochs", "option", "i", int),
    batch_size=("Size of minibatches for training LSTM", "option", "b", int),
    nr_examples=("Limit to N examples", "option", "n", int)
)
def main(model_dir=None, train_dir='test_plag_data.txt', dev_dir='dev_plag_data.txt',
         is_runtime=False,
         nr_hidden=64, max_length=100,  # Shape
         dropout=0.5, learn_rate=0.001,  # General NN config
         nb_epoch=5, batch_size=100, nr_examples=-1):  # Training params
    if model_dir is not None:
        model_dir = pathlib.Path(model_dir)
    data = read_data(train_dir)
    if is_runtime:
        dev_texts, dev_labels = read_data(dev_dir)
        acc = evaluate(model_dir, dev_texts, dev_labels, max_length=max_length)
        print(acc)
    else:
        print("Read data")
        train_labels, train_texts, train_texts2 = read_data(train_dir, limit=nr_examples)
        dev_labels, dev_texts, dev_texts2 = read_data(dev_dir, limit=nr_examples)
        train_labels = numpy.asarray(train_labels, dtype='int32')
        dev_labels = numpy.asarray(dev_labels, dtype='int32')
        lstm = train(train_texts, train_texts2, train_labels, dev_texts, dev_labels,
                     {'nr_hidden': nr_hidden, 'max_length': max_length, 'nr_class': 1},
                     {'dropout': dropout, 'lr': learn_rate},
                     {},
                     nb_epoch=nb_epoch, batch_size=batch_size)
        weights = lstm.get_weights()
        if model_dir is not None:
            with (model_dir / 'model').open('wb') as file_:
                pickle.dump(weights[1:], file_)
            with (model_dir / 'config.json').open('wb') as file_:
                file_.write(lstm.to_json())


if __name__ == '__main__':
    plac.call(main)

#NoPLag = 0
#Plag = 1