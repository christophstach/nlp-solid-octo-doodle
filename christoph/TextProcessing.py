# -*- coding: utf-8 -*-

import re

import redis
import requests

redisConnection = redis.StrictRedis(host='localhost', port=6379, db=1)
"""
Dublette: Teileweise und vollständige Wörter (= Wortgruppen) gleichheit von 
verglichenen Texten
"""

stopWordFile = open("stopwords.txt")
stopwords = stopWordFile.read().splitlines()
stopWordFile.close()

url_wortschatz_leipzig = "http://api.corpora.uni-leipzig.de/ws/words/deu_news_2012_1M/wordrelations/"

# regular expressions for stemming
stripge = re.compile(r"^ge(.{4,})")
replxx = re.compile(r"(.)\1")
replxxback = re.compile(r"(.)\*");
stripemr = re.compile(r"e[mr]$")
stripnd = re.compile(r"nd$")
stript = re.compile(r"t$")
stripesn = re.compile(r"[esn]$")


def preprocessing(text: str):
    # Sonderzeichen + HTML parsing/deletion (Marvin) - checked.
    # Reduce spaces (Ophelie) - checked sorry.
    # Stoppwörter (Marvin) - checked.

    # return removeStopWords(removeSpecialChars(text))
    # lemmatizing (Ophelie) - checked
    # make text lowercase
    text_first_steps = lemmatizing(removeStopWords(
        removeSpecialChars(text))).lower()
    # N-Gramme (Marvin) + datenbank
    return text_first_steps


def analysis(text: str):
    # TF-IDF
    # Text: Ophelie
    # Impl: Marvin
    return None


def removeSpecialChars(text: str):
    # remove special chars, clean up front numbers, spaces
    # and removes doubled spaces as well
    removedCopyright = re.sub(
        r'Mehr zum Thema[\w\s\S]*© Berliner Morgenpost [0-9]{4} – Alle Rechte vorbehalten\.',
        '', text)
    return re.sub(r'[^\w äöüÄÖÜß ]+', '',
                  removedCopyright).lstrip('0123456789-_. ').strip()


def removeSpecialCharsButLeavePunctuationMarks(text: str):
    # remove special chars, clean up front numbers, spaces
    # and removes doubled spaces as well
    # leaves punctuation marks in text
    removedCopyright = re.sub(
        r'Mehr zum Thema[\w\s\S]*© Berliner Morgenpost [0-9]{4} – Alle Rechte vorbehalten\.',
        '', text)
    return re.sub(r'[^\w äöüÄÖÜß ]+', '',
                  removedCopyright).lstrip('0123456789 ').strip()


def removeStopWords(text: str):
    finalText = text
    for stopword in stopwords:
        finalText = finalText.replace(" " + stopword + " ", " ")

    return finalText.strip()


"hallo  ich bin ..."


def lemmatizing(text: str):
    # text in 1er-Tokens splitten
    list_words_raw = text.split(" ")
    list_words_lemmatized = []
    for word in list_words_raw:
        if (word != ""):
            lemma = lemmatize_word(word)
            list_words_lemmatized.append(lemma)
            print(word, " - ", lemma)
        else:
            print("Empty Word found ...")
    # convert list to string
    text_lemmatized = ' '.join(list_words_lemmatized)
    return text_lemmatized


# lemmatizen konkreter worte
def lemmatize_word(word: str):
    lemma = check_morphy(word)

    # wenn lemma nicht in morphy gefunden dann request an wortschatz leipzig
    if lemma == "":
        lemma = request_wortschatz_leipzig(word)

    # wenn lemma nicht in leipzig corpus gefunden dann wort stemmen
    if lemma == "":
        lemma = stem(word)
        assert (lemma != '')
        # stemm in lexikon schreiben
        redisConnection.set(word, lemma)

    return decodeIfNeccessary(lemma)


# checkt ob wort in morphy-dictionary existiert
def check_morphy(word):
    redisLemma = redisConnection.get(word)

    # check if redis has lemma for word otherwise empty string
    return redisLemma if redisLemma != None else ""


# check ob wort in uni leipzig wortschatz corpora existiert
def request_wortschatz_leipzig(word):
    lemma = ""
    url = url_wortschatz_leipzig + word
    response = requests.get(url)

    if response.status_code == 200:
        json_file = response.json()

        if len(json_file) > 0:
            json_data_data = json_file[0]
            assert (json_data_data["word2"] != '')
            lemma = json_data_data["word2"]
            redisConnection.set(word, lemma)

    return lemma


# Quelle der stem-Funktion: https://github.com/LeonieWeissweiler/CISTEM/blob/master/Cistem.py
def stem(word, case_insensitive=False):
    if len(word) == 0:
        return word

    upper = word[0].isupper()
    word = word.lower()

    word = word.replace("ü", "u")
    word = word.replace("ö", "o")
    word = word.replace("ä", "a")
    word = word.replace("ß", "ss")

    word = stripge.sub(r"\1", word)
    word = word.replace("sch", "$")
    word = word.replace("ei", "%")
    word = word.replace("ie", "&")
    word = replxx.sub(r"\1*", word)

    while len(word) > 3:
        if len(word) > 5:
            (word, success) = stripemr.subn("", word)
            if success != 0:
                continue

            (word, success) = stripnd.subn("", word)
            if success != 0:
                continue

        if not upper or case_insensitive:
            (word, success) = stript.subn("", word)
            if success != 0:
                continue

        (word, success) = stripesn.subn("", word)
        if success != 0:
            continue
        else:
            break

    word = replxxback.sub(r"\1\1", word)
    word = word.replace("%", "ei")
    word = word.replace("&", "ie")
    word = word.replace("$", "sch")

    return word


def nGrammsTokenization(text: str):
    return None


def decodeIfNeccessary(s):
    if isinstance(s, str):
        return s
    else:
        return str(s, "UTF-8")
