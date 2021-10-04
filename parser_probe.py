import requests
import maya
from bs4 import BeautifulSoup
from collections import namedtuple

News = namedtuple('News', 'date source title description link media tags')


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.61 '
                         'Safari/537.36'}


def parser_n_plus_1(url):
    result = []
    page = requests.get(url, headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                    'title': news_this_source.title.text,
                    'description': news_this_source.description.text.strip(),
                    'link': news_this_source.link.text,
                    'media': str(news_this_source.find('media:content')).split('"')[3],
                    'tags': None
                    }
            result.append(news)

        return result


list_parsers = [{'name': 'N+1: научные статьи, новости, открытия',
                 'url': 'https://nplus1.ru',
                 'logo': 'https://nplus1.ru/i/logo.png',
                 'links_of_parse': ('https://nplus1.ru/rss', ),
                 'func_parser': parser_n_plus_1
                 },
                ]

if __name__ == "__main__":
    all_news = []
    for parser in list_parsers:
        all_news.extend(parser['func_parser'](*parser['links_of_parse']))

    print(*sorted(all_news, key=lambda x: x['datetime'], reverse=True), len(all_news), sep='\n')