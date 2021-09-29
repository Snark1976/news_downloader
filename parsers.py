import requests
import time
from bs4 import BeautifulSoup
from collections import namedtuple


News = namedtuple('News', 'date source title description link media')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.61 '
                         'Safari/537.36'}


def parser_n_plus_1():
    result = []
    page = requests.get('https://nplus1.ru/rss', headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-6],
                                                       "%a, %d %b %Y %H:%M:%S")) - 3 * 60 * 60,
                        source='nplus1.ru',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip(),
                        link=news_this_source.link.text,
                        media=str(news_this_source.find('media:content')).split('"')[3]
                        )
            result.append(news)

        return result


def parser_dev_by():
    result = []
    page = requests.get('https://dev.by/rss', headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-4],
                                                       "%a, %d %b %Y %H:%M:%S")),
                        source='dev.by',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip().replace('\xa0', ' '),
                        link=news_this_source.link.text,
                        media=str(news_this_source.find('enclosure')).split('"')[3]
                        )
            result.append(news)

        return result


def parser_bbc_russian():
    result = []
    page = requests.get('http://feeds.bbci.co.uk/russian/rss.xml', headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-4],
                                                       "%a, %d %b %Y %H:%M:%S")),
                        source='bbc.com/russian',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip(),
                        link=news_this_source.link.text,
                        media=None
                        )
            result.append(news)

        return result


def parser_deutsche_welle():
    result = []
    page = requests.get('https://rss.dw.com/xml/rss-ru-all', headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-4],
                                                       "%a, %d %b %Y %H:%M:%S")),
                        source='dw.com/ru',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip(),
                        link=news_this_source.link.text,
                        media=None
                        )
            result.append(news)

        return result


def parser_lenta_ru():
    result = []
    page = requests.get('https://lenta.ru/rss/', headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-6],
                                                       "%a, %d %b %Y %H:%M:%S")) - 3 * 60 * 60,
                        source='lenta.ru',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip(),
                        link=news_this_source.link.text,
                        media=str(news_this_source.find('enclosure')).split('"')[5]
                        )
            result.append(news)

        return result


def parser_century22():
    result = []
    all_news_this_source = []

    page = requests.get('https://22century.ru/news/', headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'lxml')
        all_news_this_source.append(soup.find('article', class_='article-item article-item-3_4'))
        all_news_this_source.extend(soup.find_all('article', class_='article-item article-item-1_2'))

    page = requests.get('https://22century.ru/popular-science-publications/', headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'lxml')
        all_news_this_source.append(soup.find('article', class_='article-item article-item-3_4'))
        all_news_this_source.extend(soup.find_all('article', class_='article-item article-item-1_2'))

    for news_this_source in all_news_this_source:
        news = News(date=time.mktime(time.strptime(news_this_source.select('time')[0]['datatime'],
                                                   "%Y-%m-%d")),
                    source='century22.ru',
                    title=news_this_source.select('h3.item_link a')[0].text.strip().replace('\xa0', ' '),
                    description=None,
                    link=news_this_source.select('h3.item_link a')[0]['href'],
                    media=news_this_source.select('img')[0]['src']
                    )
        result.append(news)

    return result


dict_parsers = {'https://nplus1.ru/rss': parser_n_plus_1,
                'https://dev.by/rss': parser_dev_by,
                'http://feeds.bbci.co.uk/russian/rss.xml': parser_bbc_russian,
                'https://rss.dw.com/xml/rss-ru-all': parser_deutsche_welle,
                'https://lenta.ru/rss/': parser_lenta_ru,
                'https://22century.ru/news & https://22century.ru/popular-science-publications)': parser_century22,
                }

all_news = []
for parser in dict_parsers.values():
    all_news.extend(parser())

print(*sorted(all_news, reverse=True), len(all_news), sep='\n')
