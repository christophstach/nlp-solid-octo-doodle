import logging
import urllib.request

from bs4 import BeautifulSoup


def crawl_html(data_source_url):
    soup = get_soup(data_source_url)
    title = soup.find('title').get_text()
    date_issued = get_content_from_soup(soup, 'DC.date.issued')
    last_modified = get_content_from_soup(soup, 'last-modified')
    author = get_content_from_soup(soup, 'author')
    description = get_content_from_soup(soup, 'description')
    keywords = get_content_from_soup(soup, 'keywords')
    article_body_text = get_article_body_text(soup)
    article = {"title": title, "text": article_body_text, "url": data_source_url, "author": author, "summary": description,
               "published": date_issued, "updated": last_modified, "keywords": keywords}
    return article


def get_content_from_soup(soup, name):
    content = soup.find('meta', {'name': name})
    if content and content["content"]:
        content = content["content"]
    else:
        content = ''
    return content


def get_soup(dataSourceURL):
    try:
        data_html = urllib.request.urlopen(dataSourceURL).read().decode('utf-8')
        return BeautifulSoup(data_html, 'html.parser')
    except urllib.request.HTTPError as h:
        logger = logging.getLogger("Crawler")
        error_code = str(h.code)
        if error_code == '404':
            logger.log('URL False: ' + dataSourceURL)
            pass
        else:
            logger.log('Exception: ' + format(h) + ' from url: ' + dataSourceURL)
    except urllib.request.URLError as u:
        logger = logging.getLogger("Crawler")
        logger.log('Exception: ' + format(u) + ' from url: ' + dataSourceURL)
        pass
    except Exception as e:
        logger = logging.getLogger("Crawler")
        logger.log('Exception: ' + format(e) + ' from url: ' + dataSourceURL)
        pass


def get_article_body_text(soup):
    article_body = soup.find("div", {"class": "article__body"})
    [s.extract() for s in article_body('script')]
    [s.extract() for s in article_body('style')]
    [s.extract() for s in article_body('figure')]  # removes captions
    text = article_body.get_text().replace('\n', ' ')[2:]
    return text


#dataSourceURL = "https://www.morgenpost.de/berlin/polizeibericht/article214165001/Polizei-stoppt-Raser-bei-illegalem-Autorennen.html"

#article_example = crawl_html(dataSourceURL)
