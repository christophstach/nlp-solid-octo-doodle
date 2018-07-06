import logging
import time
import traceback
import pytz

from newspaper_article import NewspaperArticle
from database_connector import *
from crawler_html import *
from crawler_rss import *

RSS_WAITING_TIME = 900
CRAWL_NEXT_ARTICLE_WAITING_TIME = 60


def init_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Crawler")
    handler = logging.FileHandler('.Crawler.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('Logging active')


def check_rss():
    try:
        logger = logging.getLogger("Crawler")
        # allows to check if RSS is actually new to us
        latest_update = pytz.utc.localize(
            datetime.datetime.utcnow()) - datetime.timedelta(1)
        while True:
            logger.info('Reading RSS-feed')
            rss_list = get_rss_feed("https://www.morgenpost.de/rss")
            rss_updated = rss_list[0]['date_feed_updated']
            if rss_list and rss_updated > latest_update:
                my_articles = rss_list[0]['rss_values']
                logger.info('Start crawling...')
                crawl_articles(my_articles)
            time.sleep(RSS_WAITING_TIME)
    except Exception:
        logger = logging.getLogger("Crawler")
        logger.error('Exception in check_rss() ' + traceback.format_exc())


def crawl_articles(list):
    try:
        logger = logging.getLogger("Crawler")
        article_counter = 0
        mongo_articles = get_articles_from_mongo_db()
        print(mongo_articles.find({}).count())
        for article in list:
            new_article = crawl_html(article['link'])
            logger.info('check if article ' + new_article['title'] +
                        ' is already known')
            if is_article_relevant(new_article, mongo_articles):
                article_counter += 1
                new_article = NewspaperArticle(
                    new_article['title'], new_article['text'],
                    new_article['url'], new_article['author'],
                    new_article['summary'], new_article['published'],
                    new_article['updated'], article['category'],
                    new_article['keywords'])
                logger.info('written article to DB')
                mongo_articles.insert_one(new_article.__dict__)
                time.sleep(CRAWL_NEXT_ARTICLE_WAITING_TIME)
        logger.info('$s mongo_articles were written do DB', article_counter)
        return
    except Exception:
        logger = logging.getLogger("Crawler")
        logger.error('Exception in check_rss() ' + traceback.format_exc())
        pass


def is_article_relevant(new_article, mongo_articles):
    if not is_article_already_in_mongo_db(new_article, mongo_articles):
        if contains_berlin(new_article):
            return True
    return False


def is_article_already_in_mongo_db(new_article, mongo_articles):
    db_article_url_matches = mongo_articles.find_one({
        'url': new_article['url']
    })
    db_article_updated_matches = update_field_exists_and_matches_or_doesnt_exist_at_all(
        mongo_articles, new_article)
    if db_article_url_matches and db_article_updated_matches:
        return True
    return False


def update_field_exists_and_matches_or_doesnt_exist_at_all(
        mongo_articles, new_article):
    try:
        if mongo_articles.find_one({
                'url': new_article['url'],
                'update': {
                    "$exists": True
                }
        }):
            db_article_updated_matches = mongo_articles.find_one({
                'url':
                new_article['url'],
                'update':
                new_article['update']
            })
            return db_article_updated_matches
        else:
            logger = logging.getLogger("Crawler")
            logger.info('No update field known for ' + new_article['url'])
        return True
    except KeyError as k:
        logger = logging.getLogger("Crawler")
        logger.error('Exception in check for updated ' +
                     traceback.format_exc())
        pass


def contains_berlin(article):
    keywords = article['keywords'].lower()
    title = article['title'].lower().replace('berliner morgenpost', '')
    text = article['text'].lower().replace('berliner morgenpost', '')
    if 'berlin' in keywords or 'berlin' in title or 'berlin' in text:
        return True
    return False


def main():
    init_logging()
    logger = logging.getLogger("Crawler")
    logger.info('Startup: start to check for RSS updates')
    try:
        check_rss()
        while True:
            time.sleep(2)
    except:
        logger.error('Error thrown in main.py(), ungraceful exit')


main()
