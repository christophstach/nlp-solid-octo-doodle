import spacy
import pprint
import random

from database_connector import *
from helper import *


nlp = spacy.load('de')

mongo_articles = get_articles_from_mongo_db()
articles = mongo_articles.find({})

#testarticle = mongo_articles.find_one()
#testtext = testarticle['text']

MAX_INDEX = mongo_articles.find({}).count()

random_german_words = open('german_words.txt', 'r').readlines(200000)

filename_out = 'train_plag_data.txt'

N_ARTICLES_IN_TRAIN_PLAG_DATA = 1050


def build_plagiarism_training_data():
    all_articles = get_all_articles()
    selected_articles = get_selected_articles(all_articles)
    other_articles = get_other_articles(all_articles)

    all_german_random_words = get_german_word_list()

    index_no_plag = 1
    index_plag = 2
    while selected_articles.__len__() >= 1:
        try:
            print(selected_articles.__len__())
            # TODO no_plag_article()
            article = selected_articles.pop(index_no_plag)
            index_no_plag = index_no_plag + 2
            training_texts = get_texts_with_no_plag_article(article, other_articles)
            write_in_training_data('NoPlag', training_texts)

            #TODO plag_article()

            random_words = get_sample_random_words(all_german_random_words)
            article = selected_articles.pop(index_plag)
            index_plag = index_plag + 2
            training_texts = get_texts_with_plag_article(article, other_articles, random_words)
            write_in_training_data('Plag', clean_comma_after_punctuation_mark(training_texts))

        except Exception as e:
            print('Exception')
            print(e.__traceback__)
            print(e.__cause__)
            pass


def write_in_training_data(label, training_texts):
    with open(filename_out, 'a') as out:
        out.write('__label__' + label + ' , ' + training_texts + '\n')


def read_train_file():
    with open('train_plag_data.txt') as f:
        read_data = f.read()
        return read_data


def write_all_training_data_at_once(data):
    with open('train_cleaned_plag_data.txt', 'a') as out:
        out.write(data)


def get_all_articles():
    all_articles = {}
    index = 1
    for a in articles:
        text = a.get('text')
        all_articles.update({index: text})
        index = index + 1
    return all_articles


def get_selected_articles(all_articles):
    selected_articles = {}
    random_index_nums = random.sample(range(1, MAX_INDEX), N_ARTICLES_IN_TRAIN_PLAG_DATA)
    index_selected = 1
    for index_random in random_index_nums:
        selected = all_articles.get(index_random)
        all_articles.pop(index_random)
        selected_articles.update({index_selected: selected})
        index_selected = index_selected + 1
    return selected_articles


def get_other_articles(all_articles):
    other_articles = {}
    index_other = 1
    while all_articles.__len__() > 0:
        other = all_articles.popitem().__getitem__(1)
        other_articles.update({index_other: other})
        index_other = index_other + 1
    return other_articles


def get_texts_with_no_plag_article(article, other_articles):
    text = clean(article)
    original = text
    similarity = 1
    no_plag_text = ''
    while similarity > 0.9:
        other = other_articles.popitem().__getitem__(1)
        no_plag_text = clean(other)
        similarity = nlp(text).similarity(nlp(no_plag_text))
    return original + ' && ' + no_plag_text


def get_texts_with_plag_article(article, other_articles, random_words):
    text = nlp(clean(article))
    original = clean(article)
    plag_text = clean_str(create_plag(text, other_articles, random_words).__str__())
    return original + ' && ' + plag_text


def create_plag(text, other_articles, random_words):
    sentences = extract_sentences(text)
    case = random.randint(0, 3)
    switcher = {
        0: random_shuffle_in_article(sentences),
        1: add_new_words(sentences, random_words),
        2: extension_with_new_sentences(sentences, other_articles),
        3: shuffle_add_extend(sentences, other_articles, random_words)
    }
    return switcher.get(case)


def extract_sentences(nlp_clean_text):
    sentences = []
    for sent in nlp_clean_text.sents:
        sentences.append(sent)
    return sentences


def random_shuffle_in_article(sentences):
    shuffled = []
    for s in sentences:
        random_index = random.randint(0, sentences.__len__()-1)
        shuffled.insert(random_index, s)
    return shuffled


def add_new_words(sentences, random_words):
    n_of_sentences = sentences.__len__()
    n_of_random_words = random_words.__len__()
    if n_of_random_words >= n_of_sentences:
        n_of_random_words = n_of_sentences - 1
    try:
        random_indexes = random.sample(range(1, n_of_sentences), n_of_random_words)
        for i in random_indexes:
            sentences.__str__().__add__(random_words.pop())
    except Exception as e:
        print('e')
        print(e)
        print('n_of_sentences')
        print(n_of_sentences)
        print('n_of_random_words')
        print(n_of_random_words)
        print('random words')
        print(random_words)
        pass
    return sentences


def extension_with_new_sentences(sentences, other_articles):
    new_sentences = get_new_sentences(other_articles)
    for new_sentence in new_sentences:
        random_index = random.randint(0, sentences.__len__() - 1)
        sentences.insert(random_index, new_sentence)
    return sentences


def get_new_sentences(other_articles):
    random_other = random.randint(1, other_articles.__len__())
    other = other_articles.pop(random_other)
    other_sentences = extract_sentences(nlp(other))
    random_indexes = get_random_indexes_for_new_sentences(other_sentences)
    random_sentences = []
    for i in random_indexes:
        random_sentences.append(other_sentences.pop(i))
    return random_sentences


def get_random_indexes_for_new_sentences(other_sentences):
    random_number = random.randint(3, 6)  # min, max number of sentences
    max_index = other_sentences.__len__() - random_number
    if random_number >= max_index:
        random_number = max_index -1
    if max_index >= 1:
        try:
            random_indexes = random.sample(range(1, max_index), random_number)
        except ValueError as v:
            print('v')
            print(v)
            print('max_index')
            print(max_index)
            print('random_number')
            print(random_number)
            pass
    else:
        random_indexes = [1]
    return random_indexes


def shuffle_add_extend(sentences, other_articles, random_words):
    with_new_words = add_new_words(sentences, random_words)
    extended = extension_with_new_sentences(with_new_words, other_articles)
    return random_shuffle_in_article(extended)


def get_sample_random_words(all_german_random_words):
    random_number = random.randint(3, 10) # min, max number of words
    random_indexes = random.sample(range(1, all_german_random_words.__len__()-random_number), random_number)
    random_words = []
    for i in random_indexes:
        random_words.append(all_german_random_words.pop(i))
    return random_words


def get_german_word_list():
    wordlist = []
    for w in random_german_words:
        wordlist.append(w.rstrip())
    return wordlist


#read_data = read_train_file()
#write_all_training_data_at_once(clean_comma_after_punctuation_mark(read_data))

build_plagiarism_training_data()
