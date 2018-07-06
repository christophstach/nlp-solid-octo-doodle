from pymongo import MongoClient


def get_articles_from_mongo_db():
    username = "user2"
    password = "ed2APwhc8BVkKba"
    database = "gruppe2"
    client = MongoClient('mongodb://%s:%s@141.45.146.247:27017/%s' %
                         (username, password, database))
    db = client[database]
    articles = db.articles
    return articles

