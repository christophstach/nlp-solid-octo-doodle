import logging
import feedparser
import datetime

#dateutil dient dazu das datum aus dem struct_time in das datetime-format umzuwandeln
from dateutil import parser


def map_category(raw_category):
    final_category = None  # es wäre auch möglich ein leeres String ("") als default-Wert einzusetzen, falls None für database problematisch ist
    if raw_category in categories_list:
        final_category = raw_category
    elif raw_category in categories_mapping:
        final_category = categories_mapping[raw_category]
    return final_category


def get_rss_feed(rss_url):
    try:
        logger = logging.getLogger("Crawler")
        feed = feedparser.parse(rss_url)
        time_now = datetime.datetime.now()
        #list with values of each article (date_published, link, id)
        articles_list = [{
            'published': parser.parse(element['published']),
            'link': element['link'],
            'id': element['id'],
            'category': map_category(element['category'])
        } for element in feed['entries']]
        #list with additional date of rss-update and request
        rss_list = [{
            'date_feed_requested':
            time_now,
            'date_feed_updated':
            parser.parse(feed['feed']['updated']),
            'rss_values':
            articles_list
        }]
        logger.info('List of articles to crawl from RSS feed is created...')
        return rss_list
    except Exception as e:
        logger = logging.getLogger("Crawler")
        logger.log('Exception: ' + format(e) + ' from rss feed, rss_url = ' +
                   rss_url)


categories_list = [
    "Berlin", "Politik", "Wirtschaft", "Sport", "Panorama", "Kultur", "Wissen"
]

categories_mapping = {
    "Polizeibericht": "Berlin",
    "Brandenburg": "Berlin",
    "Familie": "Berlin",
    "Flughafen BER": "Berlin",
    "Best of Berlin": "Berlin",
    "Mauerfall": "Berlin",
    "Kinderpost": "Berlin",
    "Schüler": "Berlin",
    "Berlin Tipps": "Berlin",
    "Bezirke": "Berlin",
    "Im Westen Berlins": "Berlin",
    "Charlottenburg-Wilmersdorf": "Berlin",
    "Friedrichshain-Kreuzberg": "Berlin",
    "Lichtenberg": "Berlin",
    "Marzahn-Hellersdorf": "Berlin",
    "Mitte": "Berlin",
    "Neukölln": "Berlin",
    "Pankow": "Berlin",
    "Reinickendorf": "Berlin",
    "Spandau": "Berlin",
    "Steglitz-Zehlendorf": "Berlin",
    "Tempelhof-Schöneberg,": "Berlin",
    "Treptow-Köpenick": "Berlin",
    "Inland": "Politik",
    "Ausland": "Politik",
    "Bundestagswahl": "Politik",
    "Air Berlin": "Wirtschaft",
    "Start-Ups Berlin": "Wirtschaft",
    "Finanzen": "Wirtschaft",
    "Karriere": "Wirtschaft",
    "Steuern": "Wirtschaft",
    "Tagesgeldkonto": "Wirtschaft",
    "Börsendaten": "Wirtschaft",
    "Hertha": "Sport",
    "1. FC Union": "Sport",
    "Eisbären": "Sport",
    "Alba": "Sport",
    "Füchse": "Sport",
    "BR Volleys": "Sport",
    "Berlin-Marathon": "Sport",
    "Fußball": "Sport",
    "Fußball Bundesliga": "Sport",
    "Leichtathletik EM": "Sport",
    "Fußball-WM": "Sport",
    "Formel 1": "Sport",
    "Nachwuchssportler des Monats": "Sport",
    "Aus aller Welt": "Panorama",
    "Stars & Promis": "Panorama",
    "Leute in Berlin": "Panorama",
    "Kino": "Kultur",
    "Berlin-History": "Kultur",
    "TV": "Kultur",
    "TV-Programm": "Kultur",
    "Gesundheit": "Wissen",
    "Ratgeber": "Wissen",
    "Wetterlexikon": "Wissen",
    "Pollenflug": "Wissen",
    "Gedächtnistraining": "Wissen",
    "Web & Technik": "Wissen",
    "Fern": "Reise & Lifestyle",
    "Nah": "Reise & Lifestyle",
    "Kleine Fluchten": "Reise & Lifestyle",
    "Leserreisen": "Reise & Lifestyle",
    "Reisewetter": "Reise & Lifestyle",
    "Badewetter": "Reise & Lifestyle",
    "Gastronomie": "Reise & Lifestyle",
    "Mode": "Reise & Lifestyle",
    "Design": "Reise & Lifestyle",
    "Wohnen": "Reise & Lifestyle",
    "Beauty": "Reise & Lifestyle",
    "Clubbing": "Reise & Lifestyle",
    "Motor": "Reise & Lifestyle",
    "Lifestyle": "Reise & Lifestyle",
}

#rss_url = 'https://www.morgenpost.de/rss'

#list_feed = get_rss_feed(rss_url)

#print(list_feed)

#mit der updated-uhrzeit koennte der artikel-crawler schauen, ob der feed überhaupt geupdatet worden ist. wenn der
#feed nicht geupdated wurde, braucht er auch gar nicht erst die ganze link-liste durchzugehen.
# -> schont ressourcen.
