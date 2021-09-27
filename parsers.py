import requests
import time
from bs4 import BeautifulSoup
from collections import namedtuple


News = namedtuple('News', 'date source title description link media')
all_news = []


def parser_n_plus_1():
    page = requests.get('https://nplus1.ru/rss')
    if page.status_code == 200:
        result = []
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')
        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-6], "%a, %d %b %Y %H:%M:%S")) - 3 * 60 * 60,
                        source='nplus1.ru',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip(),
                        link=news_this_source.link.text,
                        media=str(news_this_source.find('media:content')).split('"')[3]
                        )
            result.append(news)
        return result


def parser_dev_by():
    page = requests.get('https://dev.by/rss')
    if page.status_code == 200:
        result = []
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')
        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S")),
                        source='dev.by',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip().replace('\xa0', ' '),
                        link=news_this_source.link.text,
                        media=str(news_this_source.find('enclosure')).split('"')[3]
                        )
            result.append(news)
        return result


def parser_bbc_russian():
    page = requests.get('http://feeds.bbci.co.uk/russian/rss.xml')
    if page.status_code == 200:
        result = []
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')
        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S")),
                        source='bbc.com/russian',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip(),
                        link=news_this_source.link.text,
                        media=None
                        )
            result.append(news)
        return result


def parser_deutsche_welle():
    page = requests.get('https://rss.dw.com/xml/rss-ru-all')
    if page.status_code == 200:
        result = []
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')
        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S")),
                        source='dw.com/ru',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip(),
                        link=news_this_source.link.text,
                        media=None
                        )
            result.append(news)
        return result


def parser_lenta_ru():
    page = requests.get('https://lenta.ru/rss/')
    if page.status_code == 200:
        result = []
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')
        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-6], "%a, %d %b %Y %H:%M:%S")) - 3 * 60 * 60,
                        source='lenta.ru',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip(),
                        link=news_this_source.link.text,
                        media=str(news_this_source.find('enclosure')).split('"')[5]
                        )
            result.append(news)
        return result


dict_parsers = {'https://nplus1.ru/rss': parser_n_plus_1,
                'https://dev.by/rss': parser_dev_by,
                'http://feeds.bbci.co.uk/russian/rss.xml': parser_bbc_russian,
                'https://rss.dw.com/xml/rss-ru-all': parser_deutsche_welle,
                'https://lenta.ru/rss/': parser_lenta_ru}

for parser in dict_parsers.values():
    all_news.extend(parser())

print(*sorted(all_news, reverse=True), len(all_news), sep='\n')
