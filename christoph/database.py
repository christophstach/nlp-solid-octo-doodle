from pymongo import MongoClient


def GetArticles(local, test_run, article_count=20):
    if local:
        client = MongoClient('mongodb://localhost:27017/')
    else:
        username = "user2"
        password = "ed2APwhc8BVkKba"
        database = "gruppe2"
        client = MongoClient('mongodb://%s:%s@141.45.146.247:27017/%s' % (username, password, database))

    if test_run:
        articles_group_1 = [article for article in client['gruppe1']['articles'].find().limit(article_count)]
        articles_group_2 = [article for article in client['gruppe2']['articles'].find().limit(article_count)]
        articles_group_3 = [article for article in client['gruppe3']['articles'].find().limit(article_count)]
        articles_group_4 = [article for article in client['gruppe4']['articles'].find().limit(article_count)]
    else:
        articles_group_1 = [article for article in client['gruppe1']['articles'].find()]
        articles_group_2 = [article for article in client['gruppe2']['articles'].find()]
        articles_group_3 = [article for article in client['gruppe3']['articles'].find()]
        articles_group_4 = [article for article in client['gruppe4']['articles'].find()]

    articles = articles_group_1 + articles_group_2 + articles_group_3 + articles_group_4
    # articles = articles_group_1 + articles_group_3 + articles_group_4
    articles = list(filter(lambda article: 'text' in article, articles))

    return articles