from pymongo import MongoClient

# we all love to store userdata :)
username = "marvin"
password = "Carsten111266."
client = MongoClient(
    'mongodb://%s:%s@141.45.146.247:27017/' % (username, password))


class PreprocessedArticle:
    def __init__(self, gruppe, identifier, cleanedText=None):
        self.gruppe = gruppe
        self.identifier = identifier
        if (cleanedText != None):
            self.cleanedText = cleanedText


def get_articles_from_group(gruppe: int):
    database = "gruppe" + str(gruppe)

    db = client[database]
    articles = db.articles
    return articles


def get_all_preprocess():
    database = "gruppe2"

    db = client[database]
    preprocessed = db.preprocessed
    return preprocessed.find()


'''
Saving new preprocessed Article
'''


def savePreprocessedArticle(cleanedArticle: PreprocessedArticle):
    database = "gruppe2"
    db = client[database]
    preprocessed = db.preprocessed
    return preprocessed.insert_one(cleanedArticle.__dict__).acknowledged


def hasPreprocessedArticle(gruppe: int, identifier: str):
    db = client["gruppe2"]
    preprocessed = db.preprocessed
    return preprocessed.find(PreprocessedArticle(
        gruppe, identifier).__dict__).count() > 0
